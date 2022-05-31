# SensitivePen
Dysgraphia prediction prototype
- Collects data (Adults, Children, Dataset)
- Creates prediction windows for each proband
- Calculates features for each window
- Provides prediction framework (regression & classification)

Data
- 27 probands have been used in the final model (Adults & Children)
- Contains sentence and loop data
- 3 outliers have been identified and removed for the regression model (C14, C33, C36)
- Standard Deviation: 6.95      |       Mean: 14.89

Results

**Classification (binary)**

Sensitivity: 91 % (% of dysgraphia identified)
Specificity: 62.5 % (% of non-dysraphia identified)
Accuracy: 74 % (total accuracy)

**Regression**

RMSE (incl. outliers): 5.38
RMSE (no outliers): 4.36



