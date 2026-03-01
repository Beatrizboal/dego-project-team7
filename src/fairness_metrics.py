import pandas as pd

# Evaluate outcome disparities across sensitive groups
def approval_rate_by_group(df: pd.DataFrame, sensitive_col: str, target_col: str):
    return df.groupby(sensitive_col)[target_col].mean()


def disparate_impact(df: pd.DataFrame, sensitive_col: str, target_col: str):
    rates = approval_rate_by_group(df, sensitive_col, target_col)
    return rates.min() / rates.max()
