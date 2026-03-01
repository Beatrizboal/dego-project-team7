import pandas as pd

# Completeness checks
# Checking missing values
def check_completeness(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    return pd.DataFrame({
        "missing_count": missing_count,
        "missing_percent": missing_percent
    }).sort_values("missing_percent", ascending=False)

# Consistency checks
# Find duplicated rows
def detect_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.duplicated()]


def quantify_duplicates(df: pd.DataFrame) -> dict:
    duplicate_count = df.duplicated().sum()
    duplicate_percent = (duplicate_count / len(df)) * 100

    return {
        "duplicate_count": duplicate_count,
        "duplicate_percent": duplicate_percent
    }

# Validity Checks
# Identify invalid numeric ranges
def check_validity_ranges(df: pd.DataFrame) -> dict:
    return {
        "negative_income": df[df["financials.annual_income"] <= 0],
        "invalid_dti": df[df["financials.debt_to_income"] > 1],
        "negative_credit_history": df[df["financials.credit_history_months"] < 0]
    }


# Detect inconsistent gender values
def check_consistency_gender(df: pd.DataFrame) -> pd.Series:
    return df["applicant_info.gender"].value_counts()

# Flag unrealistic ages (<18 or >100)
def check_accuracy_age(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["age"] < 18) | (df["age"] > 100)]
