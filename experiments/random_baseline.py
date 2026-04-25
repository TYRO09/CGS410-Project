import pandas as pd
from tqdm import tqdm

from src.load_sud import load_sentences
from src.graph_builder import build_dependency_graph
from src.metrics import tree_arity, tree_depth, count_crossings
from src.random_tree import generate_random_tree_with_crossings


datasets = {
    "English": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/English/SUD_English-EWT/en_ewt-sud-train.conllu",
    "German": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/German/SUD_German-GSD/de_gsd-sud-train.conllu",
    "Hindi": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/Hindi/SUD_Hindi-HDTB/hi_hdtb-sud-train.conllu",
    "Japanese": "/Volumes/HODER/CODEX/CGS410/data/SUD_Data/Japnese/SUD_Japanese-GSD/ja_gsd-sud-train.conllu",
}

results = []

for language, path in datasets.items():

    sentences = list(load_sentences(path))

    print(f"\nProcessing {language}")

    for sentence in tqdm(sentences):

        n = len(sentence)

        # real tree
        real_graph = build_dependency_graph(sentence)

        real_arity = tree_arity(real_graph)
        real_depth = tree_depth(real_graph)
        real_crossings = count_crossings(real_graph)

        # random tree
        random_graph = generate_random_tree_with_crossings(
            n,
            real_crossings
        )

        random_arity = tree_arity(random_graph)
        random_depth = tree_depth(random_graph)

        results.append({
            "language": language,

            "real_arity": real_arity,
            "random_arity": random_arity,

            "real_depth": real_depth,
            "random_depth": random_depth
        })

df = pd.DataFrame(results)

df.to_csv("results/real_vs_random_metrics.csv", index=False)

print("Saved results to results/real_vs_random_metrics.csv")