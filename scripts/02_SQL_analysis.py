import sqlite3
import pandas as pd
import os

# Load the cleaned data from file
final_df_clean = pd.read_csv('data/processed/nhanes_cleaned.csv')

conn = sqlite3.connect('data/nhanes.db')
final_df_clean.to_sql('nhanes', conn, if_exists='replace', index=False)

# Create outputs folder if it doesn't exist
os.makedirs('outputs/tables', exist_ok=True)


# Query 1 — Average health outcomes by income group

query1 = """
SELECT 
    CASE 
        WHEN income_to_poverty_ratio < 1 THEN 'Below poverty'
        WHEN income_to_poverty_ratio < 2 THEN 'Near poverty'
        WHEN income_to_poverty_ratio < 3 THEN 'Low-middle'
        WHEN income_to_poverty_ratio < 5 THEN 'Middle'
        ELSE 'High'
    END AS income_group,
    ROUND(AVG(BPXSY_avg), 2) AS avg_systolic_bp,
    ROUND(AVG(cholesterol), 2) AS avg_cholesterol,
    ROUND(AVG(PHQ9_total), 2) AS avg_depression_score,
    COUNT(*) AS n_participants
FROM nhanes
GROUP BY income_group
ORDER BY MIN(income_to_poverty_ratio)
"""
result1 = pd.read_sql_query(query1, conn)
print("=== Average Health Outcomes by Income Group ===")
print(result1)
result1.to_csv('outputs/tables/income_health_summary.csv', index=False)


# Query 2 — Depression severity breakdown by income group

query2 = """
SELECT 
    CASE 
        WHEN income_to_poverty_ratio < 1 THEN 'Below poverty'
        WHEN income_to_poverty_ratio < 2 THEN 'Near poverty'
        WHEN income_to_poverty_ratio < 3 THEN 'Low-middle'
        WHEN income_to_poverty_ratio < 5 THEN 'Middle'
        ELSE 'High'
    END AS income_group,
    CASE
        WHEN PHQ9_total < 5 THEN 'Minimal (0-4)'
        WHEN PHQ9_total < 10 THEN 'Mild (5-9)'
        WHEN PHQ9_total < 15 THEN 'Moderate (10-14)'
        WHEN PHQ9_total < 20 THEN 'Moderately severe (15-19)'
        ELSE 'Severe (20-27)'
    END AS depression_severity,
    COUNT(*) AS n_participants
FROM nhanes
GROUP BY income_group, depression_severity
ORDER BY MIN(income_to_poverty_ratio), PHQ9_total
"""
result2 = pd.read_sql_query(query2, conn)
print("\n=== Depression Severity by Income Group ===")
print(result2)
result2.to_csv('outputs/tables/depression_severity.csv', index=False)


# Query 3 — High blood pressure risk by income group

query3 = """
SELECT 
    CASE 
        WHEN income_to_poverty_ratio < 1 THEN 'Below poverty'
        WHEN income_to_poverty_ratio < 2 THEN 'Near poverty'
        WHEN income_to_poverty_ratio < 3 THEN 'Low-middle'
        WHEN income_to_poverty_ratio < 5 THEN 'Middle'
        ELSE 'High'
    END AS income_group,
    COUNT(*) AS total,
    SUM(CASE WHEN BPXSY_avg >= 130 THEN 1 ELSE 0 END) AS elevated_bp_count,
    ROUND(SUM(CASE WHEN BPXSY_avg >= 130 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_elevated_bp
FROM nhanes
GROUP BY income_group
ORDER BY MIN(income_to_poverty_ratio)
"""
result3 = pd.read_sql_query(query3, conn)
print("\n=== Blood Pressure Risk by Income Group ===")
print(result3)
result3.to_csv('outputs/tables/bp_risk.csv', index=False)


# Query 4 — Health outcomes by age decade

query4 = """
SELECT 
    (CAST(age / 10 AS INT) * 10) AS age_decade,
    ROUND(AVG(income_to_poverty_ratio), 2) AS avg_income_ratio,
    ROUND(AVG(BPXSY_avg), 2) AS avg_bp,
    ROUND(AVG(cholesterol), 2) AS avg_cholesterol,
    ROUND(AVG(PHQ9_total), 2) AS avg_phq9,
    COUNT(*) AS n_participants
FROM nhanes
GROUP BY age_decade
ORDER BY age_decade
"""
result4 = pd.read_sql_query(query4, conn)
print("\n=== Health Outcomes by Age Decade ===")
print(result4)
result4.to_csv('outputs/tables/outcomes_by_age.csv', index=False)

# Close connection
conn.close()
print("\nAll queries complete. Results saved to outputs/tables/")
