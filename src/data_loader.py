import os
import pandas as pd
from .config import DATA_FILE

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def load_data(path: str = None, dropna: bool = False) -> pd.DataFrame:
    """
    Load CSV, normalize column names and map common categorical values.
    - path: path to csv (defaults to config.DATA_FILE)
    - dropna: whether to drop rows with NaNs
    Returns a pandas DataFrame with normalized columns.
    """
    path = path or DATA_FILE
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    df = _normalize_columns(df)

    # Map dataset (if present) to human-friendly labels
    if "dataset" in df.columns:
        df["dataset"] = df["dataset"].map({1: "liver_disease", 2: "healthy", "1": "liver_disease", "2": "healthy", "Liver Disease": "liver_disease", "Healthy": "healthy"})

    # Map gender to 1/0 (robust to multiple forms)
    if "gender" in df.columns:
        df["gender"] = df["gender"].apply(lambda x: 1 if str(x).strip().lower() in ("male", "m", "1", "true") else 0)

    if dropna:
        df = df.dropna()

    return df

def print_schema(df: pd.DataFrame):
    print("Columns and dtypes:")
    for c, t in df.dtypes.items():
        print(f" - {c}: {t}")
    print("\nTop 5 rows:")
    print(df.head())