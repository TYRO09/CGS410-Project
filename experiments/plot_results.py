import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("results/real_vs_random_metrics.csv")

# ---------- ARITY ----------
df_arity = df.melt(
    id_vars=["language"],
    value_vars=["real_arity", "random_arity"],
    var_name="type",
    value_name="arity"
)

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_arity, x="language", y="arity", hue="type")
plt.title("Real vs Random Tree Arity (SUD)")
plt.tight_layout()
plt.savefig("results/arity_comparison.png", dpi=150)


# ---------- DEPTH ----------
df_depth = df.melt(
    id_vars=["language"],
    value_vars=["real_depth", "random_depth"],
    var_name="type",
    value_name="depth"
)

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_depth, x="language", y="depth", hue="type")
plt.title("Real vs Random Tree Depth (SUD)")
plt.tight_layout()
plt.savefig("results/depth_comparison.png", dpi=150)

plt.show()