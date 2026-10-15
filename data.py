import os
import pandas as pd

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Dataset.csv")
FALLBACK_DATA_PATH = os.path.join(os.path.dirname(__file__), "Dataset.csv")

def get_data_path() -> str:
    """Returns the existing data file path."""
    if os.path.exists(DEFAULT_DATA_PATH):
        return DEFAULT_DATA_PATH
    elif os.path.exists(FALLBACK_DATA_PATH):
        return FALLBACK_DATA_PATH
    return DEFAULT_DATA_PATH

def load_data(filepath: str = None) -> pd.DataFrame:
    """Loads and standardizes the FreshChain dataset."""
    path = filepath or get_data_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    df = load_data()
    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nHead:\n", df.head())
