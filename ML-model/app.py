import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_max_pool, global_mean_pool
from torch_geometric.data import Data, Batch
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
import stanza
from langdetect import detect, LangDetectException

print("Waking up the Multilingual Parsers (This might take a moment)...")

parsers = {
    "en": spacy.load("en_core_web_sm"),
    "de": spacy.load("de_core_news_sm"),
    "ja": spacy.load("ja_core_news_sm")
}

stanza.download('hi', processors='tokenize,pos,lemma,depparse')
hi_parser = stanza.Pipeline('hi', processors='tokenize,pos,lemma,depparse', use_gpu=False)

pos_map = {"ADJ": 1, "ADP": 2, "ADV": 3, "AUX": 4, "CCONJ": 5, "DET": 6, "INTJ": 7, "NOUN": 8, "NUM": 9, "PART": 10, "PRON": 11, "PROPN": 12, "PUNCT": 13, "SCONJ": 14, "SYM": 15, "VERB": 16, "X": 17}

class DLM_Classifier(torch.nn.Module):
    def __init__(self):
        super(DLM_Classifier, self).__init__()
        self.conv1 = GCNConv(3, 32) 
        self.conv2 = GCNConv(32, 64)
        self.conv3 = GCNConv(64, 64) 
        self.classifier = torch.nn.Linear(128, 2)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index) 
        x_max = global_max_pool(x, batch) 
        x_mean = global_mean_pool(x, batch)
        x_combined = torch.cat([x_max, x_mean], dim=1) 
        out = self.classifier(x_combined)
        return F.softmax(out, dim=1) 

print("Waking up the Multilingual GNN...")
model = DLM_Classifier()
# LOAD THE NEW BABEL BRAIN
model.load_state_dict(torch.load('dlm_gnn_multilingual.pth', map_location=torch.device('cpu')))
model.eval() 

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentence():
    data = request.json
    sentence = data.get("text", "")
    
    if not sentence:
        return jsonify({"error": "No text provided"}), 400

    # ---------------------------------------------------------
    # THE UPDATED LANGUAGE DETECTION BLOCK
    # ---------------------------------------------------------
    try:
        lang_code = detect(sentence)
    except LangDetectException:
        lang_code = "en" 

    # Force short Hindi/Jap strings
    if any("\u0900" <= c <= "\u097F" for c in sentence): lang_code = "hi"
    if any("\u3040" <= c <= "\u309F" for c in sentence): lang_code = "ja"

    # THE ULTIMATE FALLBACK: Catch weird langdetect guesses
    if lang_code not in ["en", "de", "ja", "hi"]:
        lang_code = "en"
    # ---------------------------------------------------------

    sources, targets, pos_ids = [], [], []
    viz_nodes, viz_edges = [], []
    has_verb, num_roots, chaos_tags = False, 0, 0
    num_nodes = 0

    if lang_code in ["en", "de", "ja"]:
        doc = parsers[lang_code](sentence)
        num_nodes = len(doc)
        
        for token in doc:
            if token.pos_ in ["VERB", "AUX"]: has_verb = True
            if token.dep_ == "ROOT": num_roots += 1
            if token.dep_ == "dep": chaos_tags += 1
            
            pos_ids.append(pos_map.get(token.pos_, 17))
            viz_nodes.append({"id": token.i, "label": f"{token.text}\n({token.pos_})"})
            
            if token.dep_ != "ROOT":
                sources.append(token.head.i)
                targets.append(token.i)
                viz_edges.append({"from": token.head.i, "to": token.i})

    elif lang_code == "hi":
        doc = hi_parser(sentence)
        words = [word for sent in doc.sentences for word in sent.words]
        num_nodes = len(words)
        
        for i, word in enumerate(words):
            if word.upos in ["VERB", "AUX"]: has_verb = True
            if word.deprel == "root": num_roots += 1
            if word.deprel == "dep": chaos_tags += 1
            
            pos_ids.append(pos_map.get(word.upos, 17))
            viz_nodes.append({"id": i, "label": f"{word.text}\n({word.upos})"})
            
            if word.head > 0: 
                sources.append(word.head - 1)
                targets.append(i)
                viz_edges.append({"from": word.head - 1, "to": i})
    else:
        return jsonify({"error": f"Detected '{lang_code}'. Currently only EN, DE, JA, and HI are supported."}), 400

    if num_nodes < 3:
        return jsonify({"error": "Sentence too short."}), 400

    if not has_verb or num_roots != 1 or (chaos_tags / num_nodes) > 0.15:
        for node in viz_nodes:
            node["color"] = {"background": "#4c0519", "border": "#f43f5e"} 
        return jsonify({
            "sentence": sentence, "nodes": num_nodes, "human_confidence": 0.0, "random_confidence": 100.0,
            "verdict": f"Word Salad ({lang_code.upper()})", "viz_nodes": viz_nodes, "viz_edges": viz_edges
        })

    out_deg = [0] * num_nodes
    for s in sources: out_deg[s] += 1
        
    u_sources = sources + targets
    u_targets = targets + sources
    edge_index = torch.tensor([u_sources, u_targets], dtype=torch.long)
    
    features = [[out_deg[i], i / num_nodes, pos_ids[i]] for i in range(num_nodes)]
    x = torch.tensor(features, dtype=torch.float)
    
    graph = Data(x=x, edge_index=edge_index)
    batch = Batch.from_data_list([graph]) 
    
    with torch.no_grad():
        prediction = model(batch)
        
    prob_human = float(prediction[0][0]) * 100
    prob_math = float(prediction[0][1]) * 100
    
    return jsonify({
        "sentence": sentence, "nodes": num_nodes, "human_confidence": round(prob_human, 2),
        "random_confidence": round(prob_math, 2),
        "verdict": f"Optimized ({lang_code.upper()})",
        "viz_nodes": viz_nodes, "viz_edges": viz_edges
    })

if __name__ == '__main__':
    print("Multilingual Backend Online! Listening on port 7860...")
    app.run(host='0.0.0.0', port=7860)