# data_loader.py module allows to handle ingestion of raw dataset (flattening JSON)

import json
import pandas as pd


def load_raw_data(filepath: str) -> pd.DataFrame:
    with open(filepath, "r") as f: # Load raw JSON file
        raw_data = json.load(f)

    df = pd.json_normalize(raw_data) # Flatten nested JSON structure

    return df # Structured DataFrame is returned for further processing
