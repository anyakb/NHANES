# Can Your Income Predict Your Health? An Analysis of NHANES Data

A data science project exploring the relationship between income-to-poverty ratio and three key health outcomes — depression, blood pressure, and cholesterol — using the NHANES (National Health and Nutrition Examination Survey) dataset.

---

## Project Overview

This project investigates whether income-to-poverty ratio is a statistically significant predictor of mental and physical health outcomes in the United States. Using NHANES survey data, the analysis combines data cleaning, SQL aggregation, multiple regression modelling, web scraping, and data visualisation to tell a data-driven story about economic inequality and health.

**Key finding:** Higher income is significantly associated with lower depression scores (PHQ-9), even after controlling for age and education (p < 0.0001). The relationship with blood pressure and cholesterol is suggestive but less conclusive, pointing to the particular sensitivity of mental health to financial stress.

---

## Blog

The full write-up is available at: https://anyakb.github.io/NHANES/blog.html

## Repository Structure

```
NHANES-DATA-ANALYSIS/
│
├── data/
│   ├── raw/                  # Original NHANES .xpt source files (unmodified)
│   │   ├── BPXO.xpt          # Blood pressure
│   │   ├── DEMO.xpt          # Demographics
│   │   ├── DPQ.xpt           # Depression questionnaire (PHQ-9)
│   │   ├── INQ_L.xpt         # Income data
│   │   └── TCHOL.xpt         # Cholesterol
│   └── processed/            # Cleaned, analysis-ready data
│       └── nhanes_cleaned.csv
│
├── scripts/
│   ├── 01_cleaning.py        # Data cleaning and merging
│   ├── 02_SQL_analysis.py    # SQL aggregations via SQLite
│   ├── 03_regression.py      # Multiple regression models (statsmodels)
│   ├── 04_visualisations.R   # ggplot2 visualisations
│   └── 05_webscraping.py     # WHO/NHS contextual statistics scraper
│
├── outputs/
│   ├── figures/              # All generated plots (PNG, 300 DPI)
│   └── tables/               # CSV outputs from SQL and regression
│
├── README.md
└── requirements.txt
```

---

## Data Source

**Dataset:** NHANES (National Health and Nutrition Examination Survey)
**Survey cycle:** 2021-2023
**Provider:** Centers for Disease Control and Prevention (CDC), United States
**Access:** Publicly available at [https://wwwn.cdc.gov/nchs/nhanes/](https://wwwn.cdc.gov/nchs/nhanes/)

### Files used

| File | Content | Key variables used |
|------|---------|-------------------|
| DEMO.xpt | Demographics | Age (RIDAGEYR), Education (DMDEDUC2) |
| BPXO.xpt | Blood pressure | Systolic readings (BPXOSY1–3) |
| TCHOL.xpt | Cholesterol | Total cholesterol (LBXTC) |
| DPQ.xpt | Depression (PHQ-9) | Items DPQ010–DPQ090 |
| INQ_L.xpt | Income | Income-to-poverty ratio (INDFMPIR) |

All datasets are merged on the unique participant identifier **SEQN**.

---

## How to Reproduce

### 1. Download the data

Download the `.xpt` files listed above from the NHANES 2021-2023 cycle at:
[https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017)

Place all files in `data/raw/`.

### 2. Set up the Python environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3. Install R packages

Open R or RStudio and run:

```r
install.packages(c("ggplot2", "dplyr", "readr", "tidyr"))
```

### 4. Run scripts in order

```bash
python scripts/01_cleaning.py       # Produces data/processed/nhanes_cleaned.csv
python scripts/02_SQL_analysis.py   # Produces outputs/tables/
python scripts/03_regression.py     # Produces outputs/tables/regression_results.csv
Rscript scripts/04_visualisations.R # Produces outputs/figures/
python scripts/05_webscraping.py    # Produces outputs/tables/scraped_context.csv
```

---

## Data Cleaning Summary

Starting with **11,993 raw participants**, the cleaning pipeline retained **~4,138 participants** after the following steps:

1. Merged four datasets on unique participant ID (SEQN)
2. Renamed columns to human-readable variable names
3. Recoded invalid PHQ-9 responses (codes 7 = "refused", 9 = "don't know") as missing
4. Computed PHQ-9 total score — rows with any missing item excluded (`skipna=False`)
5. Converted PHQ-9 total to numeric to resolve dtype issues from SAS import
6. Selected key analysis columns and dropped rows with missing values
7. Restricted sample to adults aged 18+ (PHQ-9 not administered to minors)

**Attrition note:** The large reduction in sample size is primarily driven by PHQ-9 completion — the depression questionnaire is administered only to a subset of NHANES participants. Blood pressure missingness was also a significant factor.

---

## Analysis Summary

### SQL Aggregations (`02_SQL_analysis.py`)
Grouped average health outcomes by income band, depression severity distributions, blood pressure risk rates, and age-decade breakdowns — all via SQLite queries on the cleaned dataset.

### Multiple Regression (`03_regression.py`)
Three OLS regression models (statsmodels), each predicting one health outcome from income-to-poverty ratio, controlling for age and education:

| Outcome | Income Coefficient | p-value | R² |
|---------|-------------------|---------|-----|
| Systolic BP | +0.069 | 0.689 | 0.138 |
| Cholesterol | +0.883 | 0.057 | 0.004 |
| PHQ-9 Depression | **−0.525** | **<0.001** | 0.068 |

### Web Scraping (`05_webscraping.py`)
Scraped contextual statistics from the Mental Health Foundation, WHO, and Mental Health America to contextualise findings within the broader literature on social determinants of health.

### Visualisations (`04_visualisations.R`)
Five ggplot2 charts: bar charts, a box plot, stacked proportional bar chart, and a regression coefficient plot with significance highlighting.

---

## Dependencies

### Python
See `requirements.txt`. Key packages: `pandas`, `statsmodels`, `requests`, `beautifulsoup4`, `sqlite3`

### R
`ggplot2`, `dplyr`, `readr`, `tidyr`

---

## Limitations

- NHANES is a US dataset; findings may not generalise directly to the UK or other countries
- Cross-sectional design — cannot establish causality between income and health outcomes
- R² values are modest, suggesting important confounders (diet, lifestyle, genetics) not captured in this analysis
- PHQ-9 self-report measure is subject to response bias

---

## Blog

The full write-up and interpretation of findings is available in `blog.html`.

---

## Author

Anya Briddon
University of Exeter
