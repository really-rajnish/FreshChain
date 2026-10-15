import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

def get_default_dataset_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    primary = os.path.join(current_dir, "..", "data", "Dataset.csv")
    secondary = os.path.join(current_dir, "..", "Dataset.csv")
    if os.path.exists(primary):
        return os.path.abspath(primary)
    return os.path.abspath(secondary)

def load_raw_data(file_path: str = None) -> pd.DataFrame:
    """Loads raw dataset from file path."""
    path = file_path or get_default_dataset_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset file not found at: {path}")
    df = pd.read_csv(path)
    return df

def clean_and_standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans column names, standardizes Class column (e.g. 'BAD' -> 'Bad'),
    removes duplicates and handles null values.
    """
    df = df.copy()
    
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]
    
    # Standardize string values
    if "Fruit" in df.columns:
        df["Fruit"] = df["Fruit"].astype(str).str.strip().str.capitalize()
        
    if "Class" in df.columns:
        df["Class"] = df["Class"].astype(str).str.strip().str.capitalize()
        # Ensure only 'Good' and 'Bad'
        df["Class"] = df["Class"].replace({"Bad": "Bad", "Bad": "Bad", "Good": "Good"})
        
    # Drop full duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Fill or drop na if any
    df = df.dropna().reset_index(drop=True)
    
    return df

def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes key statistics and summary information for web rendering."""
    summary = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "columns": df.columns.tolist(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "fruits": sorted(df["Fruit"].unique().tolist()) if "Fruit" in df.columns else [],
        "classes": df["Class"].value_counts().to_dict() if "Class" in df.columns else {},
        "numeric_stats": df.describe().round(2).to_dict() if not df.empty else {},
        "sample_rows": df.head(10).to_dict(orient="records")
    }
    return summary

if __name__ == "__main__":
    df = load_raw_data()
    print("Raw shape:", df.shape)
    cleaned = clean_and_standardize_data(df)
    print("Cleaned shape:", cleaned.shape)
    summary = get_data_summary(cleaned)
    print("Summary:", summary["fruits"], summary["classes"])
