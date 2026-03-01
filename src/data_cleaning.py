import pandas as pd
import numpy as np

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


# Standardize the format of gender values
def normalize_gender(df: pd.DataFrame) -> pd.DataFrame:
    df["applicant_info.gender"] = df["applicant_info.gender"].str.upper()
    df["applicant_info.gender"] = df["applicant_info.gender"].replace({
        "M": "MALE",
        "F": "FEMALE"
    })
    return df

# Remove records with invalid income
def remove_invalid_income(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["financials.annual_income"] > 0]


# Convert date column to datetime
def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["applicant_info.date_of_birth"] = pd.to_datetime(
        df["applicant_info.date_of_birth"],
        errors="coerce",
        dayfirst=True
    )
    return df
