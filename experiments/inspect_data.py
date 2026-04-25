from src.load_sud import load_sentences
from src.graph_builder import build_dependency_graph
from src.metrics import tree_arity

file_path = "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/English/SUD_English-EWT/en_ewt-sud-train.conllu"

for sentence in load_sentences(file_path):

    G = build_dependency_graph(sentence)

    print("Edges:", list(G.edges()))
    print("Tree arity:", tree_arity(G))
    print()

    break