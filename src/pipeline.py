# Reproducible Data Engineering Pipeline
import os
from src.data_loader import load_raw_data
from src.data_cleaning import (
    convert_numeric_columns,
    impute_missing_values,
    remove_invalid_income,
    normalize_gender
)
from src.feature_engineering import calculate_age


def run_pipeline(filepath: str):
    df = load_raw_data(filepath)
    df = convert_numeric_columns(df)
    df = impute_missing_values(df)
    df = remove_invalid_income(df)
    df = normalize_gender(df)
    df = calculate_age(df)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    save_path = os.path.join(output_dir, "clean_credit_data_v1.csv")
    df.to_csv(save_path, index=False)
    return df


    """df.to_csv("data/processed/clean_credit_data_v1.csv", index=False)
    return df"""
