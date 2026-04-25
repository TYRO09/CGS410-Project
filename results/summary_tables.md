# SUD Data Experiment Summaries

Below are the formatted summary tables summarizing the dataset counts, graph structural metrics, and random baseline comparisons for the SUD v2.4 trees.

## Table 1: Dataset Overview (SUD v2.4, sentences ≤ 12 tokens)

| Language | Treebank | File | Sentences |
|---|---|---|---|
| English | SUD_English-EWT | [en_ewt-sud-train.conllu](file:///Volumes/HODER/CODEX/CGS410/data/SUD_Data/en_ewt-sud-train.conllu) | 5,624 |
| German | SUD_German-GSD | [de_gsd-sud-train.conllu](file:///Volumes/HODER/CODEX/CGS410/data/SUD_Data/de_gsd-sud-train.conllu) | 3,885 |
| Hindi | SUD_Hindi-HDTB | [hi_hdtb-sud-train.conllu](file:///Volumes/HODER/CODEX/CGS410/data/SUD_Data/hi_hdtb-sud-train.conllu) | 2,301 |
| Japanese | SUD_Japanese-GSD | [ja_gsd-sud-train.conllu](file:///Volumes/HODER/CODEX/CGS410/data/SUD_Data/ja_gsd-sud-train.conllu) | 1,586 |
| **Total** | | | **13,396** |

---

## Table 2: Real SUD Tree Metrics Summary

| Language | Metric | Mean | Std | Min | Median | Max |
|---|---|---|---|---|---|---|
| English | arity | 2.67 | 1.45 | 0 | 3.0 | 8 |
| English | depth | 2.54 | 1.63 | 0 | 2.0 | 8 |
| German | arity | 3.74 | 0.95 | 1 | 4.0 | 9 |
| German | depth | 3.31 | 1.11 | 1 | 3.0 | 8 |
| Hindi | arity | 3.37 | 0.88 | 0 | 3.0 | 7 |
| Hindi | depth | 4.22 | 1.33 | 0 | 4.0 | 9 |
| Japanese | arity | 3.06 | 1.08 | 1 | 3.0 | 11 |
| Japanese | depth | 4.01 | 1.76 | 1 | 4.0 | 10 |

---

## Table 3: Real vs Random Baseline Comparison (Mean ± Std)

| Language | Real Arity | Rand Arity | Δ Arity | Real Depth | Rand Depth | Δ Depth |
|---|---|---|---|---|---|---|
| English | 2.67 ± 1.45 | 2.24 ± 1.23 | +0.42 | 2.54 ± 1.63 | 2.85 ± 1.84 | -0.31 |
| German | 3.74 ± 0.95 | 2.97 ± 0.94 | +0.77 | 3.31 ± 1.11 | 4.04 ± 1.41 | -0.73 |
| Hindi | 3.37 ± 0.88 | 3.05 ± 0.92 | +0.32 | 4.22 ± 1.33 | 4.33 ± 1.38 | -0.10 |
| Japanese | 3.06 ± 1.08 | 2.86 ± 0.94 | +0.20 | 4.01 ± 1.76 | 3.86 ± 1.49 | +0.15 |
| **Overall** | **3.15 ± 1.27** | **2.67 ± 1.13** | **+0.48** | **3.22 ± 1.61** | **3.57 ± 1.73** | **-0.34** |

> [!NOTE] 
> Δ represents the metric difference (Real - Random). Positive Δ in Arity means real trees branch out more horizontally. Negative Δ in Depth indicates real trees are shallower vertically compared to random configurations.
