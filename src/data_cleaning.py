import pandas as pd
import numpy as np

#Convert financial columns to numeric. Invalid values become NaN.
def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    numeric_columns = [
        "financials.annual_income",
        "financials.debt_to_income",
        "financials.credit_history_months"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "", regex=False).str.replace("$", "", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# Handling missing values
def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Numerical columns → median
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Categorical columns → "Unknown"
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    return df


# Remove invalid financial records
def remove_invalid_income(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["financials.annual_income"] > 0]

# Standardize gender categories
def normalize_gender(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    df["applicant_info.gender"] = df["applicant_info.gender"].str.upper()
    df["applicant_info.gender"] = df["applicant_info.gender"].replace({
        "M": "MALE",
        "F": "FEMALE"
    })
    return df

# Convert date column to datetime
def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["applicant_info.date_of_birth"] = pd.to_datetime(
        df["applicant_info.date_of_birth"],
        errors="coerce",
        dayfirst=True
    )
    return df
