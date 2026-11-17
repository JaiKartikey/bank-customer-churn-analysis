# Every number on the CV, and how to reproduce it

| CV claim | Value | Where it comes from |
| --- | --- | --- |
| Customers analyzed | 10,000 | `SELECT COUNT(*) FROM cust` |
| Churn rate | 20.4% (2,037) | `AVG(Exited)` |
| Inactive vs active churn | 26.9% vs 14.3% | `GROUP BY IsActiveMember` |
| Churn age 50-59 vs 18-29 | 56.0% vs 7.6% | `CASE WHEN` age bands, `GROUP BY` |
| Tests significant | p < 0.001 | `stats_tests.py`: Welch t-test on Age and Balance, chi-square on IsActiveMember and NumOfProducts vs Exited |
| Early-warning rule | 17.7% of customers, 40.9% of churners | `WHERE IsActiveMember=0 AND Age BETWEEN 40 AND 59` |
| Balances held by churners | 24.3% | `SUM(Balance) where Exited=1 / SUM(Balance)` |

The logistic regression in `stats_tests.py` is extra exploration and is not used on the CV.
