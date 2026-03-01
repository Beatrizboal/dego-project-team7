from src.data_loader import load_raw_data
from src.data_validation import check_completeness
from src.data_cleaning import (
    impute_missing_values,
    remove_invalid_income,
    normalize_gender
)

from src.feature_engineering import calculate_age


def run_pipeline(filepath: str):

    df = load_raw_data(filepath)

    # Cleaning
    df = impute_missing_values(df)
    df = remove_invalid_income(df)
    df = normalize_gender(df)
    df = calculate_age(df)

    # Save versioned output
    df.to_csv("data/processed/clean_credit_data_v1.csv", index=False)

    return df
