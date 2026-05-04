"""
NHANES Regression Analysis
===========================
Runs three multiple regression models to examine the relationship between
income-to-poverty ratio and each health outcome (blood pressure, cholesterol,
depression), controlling for age and education.

Input:  data/cleaned/nhanes_cleaned.csv
Output: outputs/tables/regression_results.csv
"""

import pandas as pd
import statsmodels.api as sm
import os

# Load data
df = pd.read_csv('data/processed/nhanes_cleaned.csv')

os.makedirs('outputs/tables', exist_ok=True)

# Define predictors
# Controls: age, education
# Key predictor: income_to_poverty_ratio

predictors = ['income_to_poverty_ratio', 'age', 'education']
X = df[predictors].copy()
X = sm.add_constant(X)  # adds intercept term


# Model 1 — Income predicting Systolic Blood Pressure

y_bp = df['BPXSY_avg']
model_bp = sm.OLS(y_bp, X).fit()

print("=" * 60)
print("MODEL 1: Income → Systolic Blood Pressure")
print("=" * 60)
print(model_bp.summary())


# Model 2 — Income predicting Cholesterol

y_chol = df['cholesterol']
model_chol = sm.OLS(y_chol, X).fit()

print("\n" + "=" * 60)
print("MODEL 2: Income → Cholesterol")
print("=" * 60)
print(model_chol.summary())


# Model 3 — Income predicting Depression (PHQ-9)

y_phq = df['PHQ9_total']
model_phq = sm.OLS(y_phq, X).fit()

print("\n" + "=" * 60)
print("MODEL 3: Income → Depression (PHQ-9)")
print("=" * 60)
print(model_phq.summary())


# Save a clean summary table of key results

summary_data = []

for outcome, model in zip(
    ['Systolic BP', 'Cholesterol', 'PHQ9 Depression'],
    [model_bp, model_chol, model_phq]
):
    row = {
        'outcome': outcome,
        'income_coef': round(model.params['income_to_poverty_ratio'], 4),
        'income_pvalue': round(model.pvalues['income_to_poverty_ratio'], 4),
        'age_coef': round(model.params['age'], 4),
        'age_pvalue': round(model.pvalues['age'], 4),
        'r_squared': round(model.rsquared, 4),
        'n_observations': int(model.nobs)
    }
    summary_data.append(row)

summary_df = pd.DataFrame(summary_data)
print("\n=== Regression Summary Table ===")
print(summary_df)
summary_df.to_csv('outputs/tables/regression_results.csv', index=False)
print("\nRegression results saved to outputs/tables/regression_results.csv")

print(model_phq.conf_int())

# Save confidence intervals for R
ci_data = []
for outcome, model in zip(
    ['Systolic BP', 'Cholesterol', 'PHQ9 Depression'],
    [model_bp, model_chol, model_phq]
):
    ci = model.conf_int().loc['income_to_poverty_ratio']
    ci_data.append({
        'outcome': outcome,
        'income_coef': round(model.params['income_to_poverty_ratio'], 4),
        'ci_lower': round(ci[0], 4),
        'ci_upper': round(ci[1], 4),
        'significant': model.pvalues['income_to_poverty_ratio'] < 0.05
    })

