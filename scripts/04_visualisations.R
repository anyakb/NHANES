# ============================================================
# NHANES Visualisations
# ============================================================

# Produces ggplot2 charts blog!
# Input:  outputs/tables/ (CSV files from SQL + regression)
# Output: outputs/figures/

library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)

# Create output folder
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

# Load data
nhanes <- read_csv("data/processed/nhanes_cleaned.csv")
income_summary <- read_csv("outputs/tables/income_health_summary.csv")
depression_severity <- read_csv("outputs/tables/depression_severity.csv")
bp_risk <- read_csv("outputs/tables/bp_risk.csv")
regression <- read_csv("outputs/tables/regression_results.csv")


# Consistent theme for all plots

nhanes_theme <- theme_minimal(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold", size = 15, margin = margin(b = 8)),
    plot.subtitle = element_text(colour = "#555555", size = 11, margin = margin(b = 12)),
    plot.caption  = element_text(colour = "#888888", size = 9),
    axis.title    = element_text(face = "bold", size = 11),
    panel.grid.minor = element_blank(),
    legend.position = "bottom",
    plot.margin   = margin(16, 16, 16, 16)
  )

# Set income group order (low to high)
income_order <- c("Below poverty", "Near poverty", "Low-middle", "Middle", "High")

income_summary$income_group <- factor(income_summary$income_group, levels = income_order)
depression_severity$income_group <- factor(depression_severity$income_group, levels = income_order)
bp_risk$income_group <- factor(bp_risk$income_group, levels = income_order)


# Plot 1 — Depression score by income group (bar chart)

p1 <- ggplot(income_summary, aes(x = income_group, y = avg_depression_score, fill = income_group)) +
  geom_col(width = 0.65, show.legend = FALSE) +
  geom_text(aes(label = round(avg_depression_score, 1)),
            vjust = -0.5, fontface = "bold", size = 4) +
  scale_fill_manual(values = c(
    "Below poverty" = "#c0392b",
    "Near poverty"  = "#e67e22",
    "Low-middle"    = "#f1c40f",
    "Middle"        = "#2ecc71",
    "High"          = "#27ae60"
  )) +
  labs(
    title    = "Higher Income, Lower Depression",
    subtitle = "Average PHQ-9 depression score by income-to-poverty group",
    x        = "Income-to-poverty ratio group",
    y        = "Average PHQ-9 score"
  ) +
  nhanes_theme

ggsave("outputs/figures/01_depression_by_income.png", p1, width = 10, height = 6, dpi = 300)
print(p1)

# ============================================================
# NHANES Visualisations
# ============================================================
# Produces polished ggplot2 charts for the blog
# Input:  outputs/tables/ (CSV files from SQL + regression)
# Output: outputs/figures/
# ============================================================

library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)

# Create output folder
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

# Load data
nhanes <- read_csv("data/processed/nhanes_cleaned.csv")
income_summary <- read_csv("outputs/tables/income_health_summary.csv")
depression_severity <- read_csv("outputs/tables/depression_severity.csv")
bp_risk <- read_csv("outputs/tables/bp_risk.csv")
regression <- read_csv("outputs/tables/regression_results.csv")

# ============================================================
# Consistent theme for all plots
# ============================================================
nhanes_theme <- theme_minimal(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold", size = 15, margin = margin(b = 8)),
    plot.subtitle = element_text(colour = "#555555", size = 11, margin = margin(b = 12)),
    plot.caption  = element_text(colour = "#888888", size = 9),
    axis.title    = element_text(face = "bold", size = 11),
    panel.grid.minor = element_blank(),
    legend.position = "bottom",
    plot.margin   = margin(16, 16, 16, 16)
  )

# Set income group order (low to high)
income_order <- c("Below poverty", "Near poverty", "Low-middle", "Middle", "High")

income_summary$income_group <- factor(income_summary$income_group, levels = income_order)
depression_severity$income_group <- factor(depression_severity$income_group, levels = income_order)
bp_risk$income_group <- factor(bp_risk$income_group, levels = income_order)

# Plot 2 — Blood pressure risk by income group

p2 <- ggplot(bp_risk, aes(x = income_group, y = pct_elevated_bp, fill = income_group)) +
  geom_col(width = 0.65, show.legend = FALSE) +
  geom_text(aes(label = paste0(pct_elevated_bp, "%")),
            vjust = -0.5, fontface = "bold", size = 4) +
  scale_fill_manual(values = c(
    "Below poverty" = "#c0392b",
    "Near poverty"  = "#e67e22",
    "Low-middle"    = "#f1c40f",
    "Middle"        = "#2ecc71",
    "High"          = "#27ae60"
  )) +
  labs(
    title    = "Lower Income Groups Face Higher Blood Pressure Risk",
    subtitle = "% of participants with systolic BP ≥ 130 mmHg (elevated threshold)",
    x        = "Income Group",
    y        = "% with Elevated Blood Pressure",
    caption  = "Source: NHANES. Elevated BP defined as systolic ≥ 130 mmHg (AHA guidelines)"
  ) +
  nhanes_theme

ggsave("outputs/figures/02_bp_risk_by_income.png", p2, width = 8, height = 5, dpi = 300)
cat("Saved: 02_bp_risk_by_income.png\n")


# Plot 3 — Depression severity stacked bar by income group

severity_order <- c("Minimal (0-4)", "Mild (5-9)", "Moderate (10-14)",
                    "Moderately severe (15-19)", "Severe (20-27)")

depression_severity$depression_severity <- factor(depression_severity$depression_severity,
                                                   levels = severity_order)
depression_severity$income_group <- factor(depression_severity$income_group,
                                            levels = income_order)

# Calculate percentage within each income group
depression_severity <- depression_severity %>%
  group_by(income_group) %>%
  mutate(pct = round(n_participants / sum(n_participants) * 100, 1))

p3 <- ggplot(depression_severity,
             aes(x = income_group, y = pct, fill = depression_severity)) +
  geom_col(position = "stack", width = 0.65) +
  scale_fill_manual(values = c(
    "Minimal (0-4)"             = "#27ae60",
    "Mild (5-9)"                = "#f1c40f",
    "Moderate (10-14)"          = "#e67e22",
    "Moderately severe (15-19)" = "#e74c3c",
    "Severe (20-27)"            = "#8e1010"
  )) +
  labs(
    title    = "Depression Severity Worsens at Lower Income Levels",
    subtitle = "Distribution of PHQ-9 severity categories by income group",
    x        = "Income Group",
    y        = "Percentage of Group (%)",
    fill     = "Depression Severity",
    caption  = "Source: NHANES"
  ) +
  nhanes_theme

ggsave("outputs/figures/03_depression_severity_stacked.png", p3, width = 9, height = 5, dpi = 300)
cat("Saved: 03_depression_severity_stacked.png\n")


# Plot 4 — Cholesterol distribution by income group (box plot)

nhanes$income_group <- cut(
  nhanes$income_to_poverty_ratio,
  breaks = c(0, 1, 2, 3, 5, Inf),
  labels = c("Below poverty", "Near poverty", "Low-middle", "Middle", "High")
)

nhanes$income_group <- factor(nhanes$income_group, levels = income_order)

p4 <- ggplot(nhanes %>% filter(!is.na(income_group)),
             aes(x = income_group, y = cholesterol, fill = income_group)) +
  geom_boxplot(width = 0.5, outlier.alpha = 0.2, outlier.size = 1,
               show.legend = FALSE) +
  stat_summary(fun = mean, geom = "point", shape = 18,
               size = 3, colour = "white") +
  scale_fill_manual(values = c(
    "Below poverty" = "#c0392b",
    "Near poverty"  = "#e67e22",
    "Low-middle"    = "#f1c40f",
    "Middle"        = "#2ecc71",
    "High"          = "#27ae60"
  )) +
  labs(
    title    = "Cholesterol Distribution Across Income Groups",
    subtitle = "Box plot of total cholesterol (mg/dL) — diamond shows group mean",
    x        = "Income Group",
    y        = "Total Cholesterol (mg/dL)",
    caption  = "Source: NHANES. Outliers shown as faded points"
  ) +
  nhanes_theme

ggsave("outputs/figures/04_cholesterol_boxplot.png", p4, width = 8, height = 5, dpi = 300)
cat("Saved: 04_cholesterol_boxplot.png\n")

# Plot 5 — Regression coefficients (income effect on each outcome)

p5 <- ggplot(regression, aes(x = outcome, y = income_coef, fill = income_pvalue < 0.05)) +
  geom_col(width = 0.5) +
  geom_hline(yintercept = 0, linetype = "dashed", colour = "#888888") +
  scale_fill_manual(values = c("TRUE" = "#2980b9", "FALSE" = "#bdc3c7"),
                    labels = c("TRUE" = "Significant (p < 0.05)",
                               "FALSE" = "Not significant"),
                    name = "") +
  labs(
    title    = "Effect of Income on Health Outcomes",
    subtitle = "Regression coefficients — controlling for age and education",
    x        = "Health Outcome",
    y        = "Income Coefficient",
    caption  = "Blue = statistically significant (p < 0.05). Source: NHANES"
  ) +
  nhanes_theme

ggsave("outputs/figures/05_regression_coefficients.png", p5, width = 8, height = 5, dpi = 300)
cat("Saved: 05_regression_coefficients.png\n")

cat("\nAll plots saved to outputs/figures/\n")