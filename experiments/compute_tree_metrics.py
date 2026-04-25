import pandas as pd
from tqdm import tqdm

from src.load_sud import load_sentences
from src.graph_builder import build_dependency_graph
from src.metrics import tree_arity, tree_depth


datasets = {
    "English": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/English/SUD_English-EWT/en_ewt-sud-train.conllu",
    "German": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/German/SUD_German-GSD/de_gsd-sud-train.conllu",
    "Hindi": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/Hindi/SUD_Hindi-HDTB/hi_hdtb-sud-train.conllu",
    "Japanese": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/Japnese/SUD_Japanese-GSD/ja_gsd-sud-train.conllu",
}

results = []

for language, path in datasets.items():

    sentences = list(load_sentences(path))

    print(f"Processing {language}")

    for sentence in tqdm(sentences):

        G = build_dependency_graph(sentence)

        results.append({
            "language": language,
            "arity": tree_arity(G),
            "depth": tree_depth(G)
        })

df = pd.DataFrame(results)

df.to_csv("results/tree_metrics_real.csv", index=False)

print("Saved results/tree_metrics_real.csv")