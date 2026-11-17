"""Stats layer for the bank churn project: t-test, chi-square, logistic regression.
Run: python stats_tests.py   (expects data/Churn_Modelling.csv)"""
import sys, pandas as pd
from scipy import stats
import statsmodels.api as sm

df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/Churn_Modelling.csv")

# 1. t-test: are churners older than retained customers? (Welch's t-test, unequal variances)
ch, st = df[df.Exited == 1], df[df.Exited == 0]
t, p = stats.ttest_ind(ch.Age, st.Age, equal_var=False)
print(f"Age  churned={ch.Age.mean():.1f}  retained={st.Age.mean():.1f}  t={t:.1f}  p={p:.2e}")
t, p = stats.ttest_ind(ch.Balance, st.Balance, equal_var=False)
print(f"Balance churned={ch.Balance.mean():.0f}  retained={st.Balance.mean():.0f}  t={t:.1f}  p={p:.2e}")

# 2. chi-square: is churn independent of being an active member?
tab = pd.crosstab(df.IsActiveMember, df.Exited)
chi2, p, dof, _ = stats.chi2_contingency(tab)
print(f"Chi-square IsActiveMember vs Exited: chi2={chi2:.1f} dof={dof} p={p:.2e}")
tab = pd.crosstab(df.NumOfProducts, df.Exited)
chi2, p, dof, _ = stats.chi2_contingency(tab)
print(f"Chi-square NumOfProducts vs Exited: chi2={chi2:.1f} dof={dof} p={p:.2e}")

# 3. Logistic regression: which drivers matter, holding others fixed? Odds ratios are easy to explain.
X = df[["CreditScore", "Age", "Tenure", "Balance", "IsActiveMember", "HasCrCard", "EstimatedSalary"]].copy()
X["Balance"] = X["Balance"] / 10000          # per 10k
X["EstimatedSalary"] = X["EstimatedSalary"] / 10000
X["CreditScore"] = X["CreditScore"] / 100     # per 100 points
X = pd.concat([X, pd.get_dummies(df.NumOfProducts.clip(upper=3), prefix="products", drop_first=True, dtype=float)], axis=1)
m = sm.Logit(df.Exited, sm.add_constant(X)).fit(disp=0)
out = pd.DataFrame({"odds_ratio": m.params.apply(lambda b: round(float(__import__('math').exp(b)), 2)), "p_value": m.pvalues.round(4)})
print(out.drop("const").sort_values("odds_ratio", ascending=False).to_string())
