# Compute age from date of birth
import pandas as pd


def calculate_age(df: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today()

    df["applicant_info.date_of_birth"] = pd.to_datetime(
        df["applicant_info.date_of_birth"],
        errors="coerce"
    )

    df["age"] = (
        (today - df["applicant_info.date_of_birth"]).dt.days // 365
    )

    return df
