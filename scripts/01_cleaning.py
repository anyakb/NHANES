"""
NHANES Data Cleaning Script
============================
Merges and cleans four NHANES survey datasets (demographics, blood pressure,
cholesterol, depression/PHQ-9) into a single analysis-ready CSV.

Inputs:  DEMO.xpt, BPXO.xpt, TCHOL.xpt, DPQ.xpt (NHANES [your cycle, e.g. 2017-2018])
Output:  nhanes_cleaned.csv

Steps:
    1. Load raw .xpt files
    2. Merge on participant ID (SEQN)
    3. Rename and select key variables
    4. Recode invalid PHQ-9 responses (7/9) as missing
    5. Compute PHQ-9 total score
    6. Drop rows with missing values in key variables
    7. Restrict to adults aged 18+
"""

import pandas as pd
from functools import reduce
 
 # Loading datasets
demo_df = pd.read_sas('DEMO.xpt')   # Demographics
bp_df = pd.read_sas('BPXO.xpt')     # Blood pressure
chol_df = pd.read_sas('TCHOL.xpt')  # Cholesterol
phq9_df = pd.read_sas('DPQ.xpt')    # Depression questionnaire

# Merging datasets on 'SEQN' (unique participant identifier)
data_frames = [demo_df, bp_df, chol_df, phq9_df]
merged_df = reduce(lambda left, right: pd.merge(left, right, on='SEQN', how='outer'), data_frames)

# Renaming columns
rename_dict = {
    'SEQN': 'participant_id',
    'RIDAGEYR': 'age',
    'INDFMPIR': 'income_to_poverty_ratio',
    'DMDEDUC2': 'education',
    'LBXTC': 'cholesterol'
}
merged_df.rename(columns=rename_dict, inplace=True)

# Calculating average blood pressure
bp_cols = [col for col in merged_df.columns if col.startswith('BPX')]
merged_df['BPXSY_avg'] = merged_df[[col for col in bp_cols if 'OSY' in col]].mean(axis=1)

# Handling DPQ columns (depression questionnaire)
dpq_cols = [f'DPQ0{i}0' for i in range(1, 10)]

# Recode DPQ responses: 1-4 are valid, 7 and 9 are missing
for col in dpq_cols:
    merged_df[col] = merged_df[col].replace({7: pd.NA, 9: pd.NA})

# Selecting relevant columns
keep_cols = ['participant_id', 'age', 'income_to_poverty_ratio', 'BPXSY_avg', 'education', 'cholesterol'] + dpq_cols
final_df = merged_df[keep_cols].copy()

# Calculating total PHQ-9 score, skipna=False ensures that if any item is missing, the total is also missing
final_df['PHQ9_total'] = final_df[dpq_cols].sum(axis=1, skipna=False)
final_df['PHQ9_total'] = pd.to_numeric(final_df['PHQ9_total'], errors='coerce')

# Dropping rows with missing values in key columns
key_cols_to_check = ['age', 'income_to_poverty_ratio', 'BPXSY_avg', 'education', 'cholesterol', 'PHQ9_total']
final_df_clean = final_df.dropna(subset=key_cols_to_check)

# Filtering out participants under 18 (PHQ-9 is only valid for adults)
final_df_clean = final_df_clean[final_df_clean['age'] >= 18]

# Saving cleaned dataset
final_df_clean.to_csv('nhanes_cleaned.csv', index=False)

# Basic checks
print(f"Rows before cleaning: {len(merged_df)}")
print(f"Rows after cleaning: {len(final_df_clean)}")
print(final_df_clean.describe())
assert final_df_clean.isnull().sum().sum() == 0, "Unexpected nulls remain"
print("Data cleaned successfully and saved to 'nhanes_cleaned.csv'.")

print(final_df_clean['PHQ9_total'].describe())