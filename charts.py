"""Make the 3 story charts for the bank churn project. Run: python charts.py data/Churn_Modelling.csv"""
import sys, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/Churn_Modelling.csv")
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False})
df["age_band"] = pd.cut(df.Age, [17, 29, 39, 49, 59, 100], labels=["18-29", "30-39", "40-49", "50-59", "60+"])
for col, title, fn in [("age_band", "Churn rate by age band, %", "chart1_churn_by_age.png"),
                       ("NumOfProducts", "Churn rate by number of products held, %", "chart2_churn_by_products.png")]:
    r = df.groupby(col, observed=True).Exited.mean().mul(100)
    fig, ax = plt.subplots(figsize=(6, 3.5)); b = ax.bar(r.index.astype(str), r.values, color="#2f6db5"); ax.bar_label(b, fmt="%.1f")
    ax.axhline(df.Exited.mean()*100, ls="--", color="grey"); ax.set_title(title + " (dashed = overall)"); fig.tight_layout(); fig.savefig(fn)
r = df.assign(act=df.IsActiveMember.map({1: "Active", 0: "Inactive"})).groupby(["age_band", "act"], observed=True).Exited.mean().mul(100).unstack()
fig, ax = plt.subplots(figsize=(6, 3.5)); r.plot.bar(ax=ax, color=["#9bb4d6", "#c8442f"], rot=0); ax.set_title("Churn %, active vs inactive members by age"); ax.set_xlabel("")
fig.tight_layout(); fig.savefig("chart3_activity_by_age.png"); print("saved 3 charts")
