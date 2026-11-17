-- Bank customer churn: load + quality + churn rate by segment (DuckDB / standard SQL)
CREATE OR REPLACE TABLE cust AS SELECT * FROM read_csv_auto('data/Churn_Modelling.csv');

-- Quality checks
SELECT COUNT(*) n, SUM(CASE WHEN Age IS NULL OR Balance IS NULL OR CreditScore IS NULL THEN 1 ELSE 0 END) nulls,
       MIN(Age) min_age, MAX(Age) max_age, MIN(CreditScore) min_cs, MAX(CreditScore) max_cs,
       SUM(CASE WHEN Balance=0 THEN 1 ELSE 0 END) zero_balance
FROM cust;

-- Overall churn
SELECT COUNT(*) customers, SUM(Exited) churned, ROUND(100.0*AVG(Exited),1) churn_pct FROM cust;

-- Churn by number of products
SELECT NumOfProducts, COUNT(*) customers, ROUND(100.0*AVG(Exited),1) churn_pct
FROM cust GROUP BY 1 ORDER BY 1;

-- Churn by age band
SELECT CASE WHEN Age<30 THEN '18-29' WHEN Age<40 THEN '30-39' WHEN Age<50 THEN '40-49'
            WHEN Age<60 THEN '50-59' ELSE '60+' END age_band,
       COUNT(*) customers, ROUND(100.0*AVG(Exited),1) churn_pct
FROM cust GROUP BY 1 ORDER BY 1;

-- Churn by activity
SELECT CASE WHEN IsActiveMember=1 THEN 'Active' ELSE 'Inactive' END activity,
       COUNT(*) customers, ROUND(100.0*AVG(Exited),1) churn_pct
FROM cust GROUP BY 1;

-- Churn by balance band
SELECT CASE WHEN Balance=0 THEN '0' WHEN Balance<100000 THEN '<100k' ELSE '100k+' END balance_band,
       COUNT(*) customers, ROUND(100.0*AVG(Exited),1) churn_pct
FROM cust GROUP BY 1 ORDER BY 1;

-- Balances lost to churn (deposits at risk)
SELECT ROUND(SUM(CASE WHEN Exited=1 THEN Balance ELSE 0 END),0) churned_balance,
       ROUND(100.0*SUM(CASE WHEN Exited=1 THEN Balance ELSE 0 END)/SUM(Balance),1) pct_of_total_balance
FROM cust;

-- High-risk segment rule: inactive and aged 40-59
SELECT COUNT(*) customers, ROUND(100.0*AVG(Exited),1) churn_pct,
       ROUND(100.0*SUM(Exited)/(SELECT SUM(Exited) FROM cust),1) pct_of_all_churners
FROM cust WHERE IsActiveMember=0 AND Age BETWEEN 40 AND 59;
