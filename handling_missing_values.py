import pandas as pd
import scipy.stats as stats
from itertools import combinations
from pandas.api.types import is_list_like
import numpy as np


# Cramer's V implementation
def cramers_v(confusion_matrix):
    chi2, _, _, _ = stats.chi2_contingency(confusion_matrix)
    n = confusion_matrix.sum().sum()
    k = min(confusion_matrix.shape)  # min(#rows, #cols)
    return np.sqrt(chi2 / (n * (k - 1))) if k > 1 else 0

# 1. Calculate chi squared value and Cramer's V
def test_missing_values(df):
    dfm = pd.DataFrame()
    for col in df.columns:
        if df[col].apply(lambda x: is_list_like(x)).any():
            df[col] = df[col].apply(lambda x: ' '.join(sorted(x)) if isinstance(x, list) else None)

        if df[col].isnull().sum() !=0:
            dfm[f"missing_{col}"] = df[col].isnull().astype(int)
                # Example: Test relationship with 'industry'
    for col_m in dfm:
        for col in df:
            contingency = pd.crosstab(dfm[col_m], df[col])
            chi2, p, dof, expected = stats.chi2_contingency(contingency)
            v = cramers_v(contingency)
            if v > 0.8 and p < 0.05:
                print(f"\n🔍 Columns: '{col_m}', {col}")
                print(f"Chi-squared p-value: {p}")
                print(f"Cramér's V: {v:.4f}")




