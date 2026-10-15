import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from typing import Tuple, Dict, Any, List

CATEGORICAL_FEATURES = ["Fruit"]
NUMERICAL_FEATURES = ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"]
TARGET_COLUMN = "Class"

def build_preprocessor() -> ColumnTransformer:
    """Builds a scikit-learn ColumnTransformer for categorical and numerical features."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor

def prepare_features_and_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Splits dataframe into feature matrix X and binary target vector y."""
    X = df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES].copy()
    # Map Good -> 1, Bad -> 0
    y = (df[TARGET_COLUMN] == "Good").astype(int)
    return X, y

def get_train_test_data(
    df: pd.DataFrame, 
    test_size: float = 0.2, 
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Prepares stratified train-test splits."""
    X, y = prepare_features_and_target(df)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def inspect_transformed_features(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Transforms sample data to let users inspect feature scaling & one-hot encoding columns.
    """
    X, y = prepare_features_and_target(df)
    preprocessor = build_preprocessor()
    X_trans = preprocessor.fit_transform(X)
    
    # Get encoded feature names
    cat_encoder = preprocessor.named_transformers_["cat"]
    encoded_cat_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    all_feature_names = NUMERICAL_FEATURES + encoded_cat_names
    
    transformed_df = pd.DataFrame(X_trans, columns=all_feature_names)
    
    return {
        "raw_features": CATEGORICAL_FEATURES + NUMERICAL_FEATURES,
        "encoded_feature_names": all_feature_names,
        "num_features_before": len(CATEGORICAL_FEATURES + NUMERICAL_FEATURES),
        "num_features_after": len(all_feature_names),
        "scaling_method": "StandardScaler (Mean=0, Std=1)",
        "encoding_method": "One-Hot Encoding",
        "sample_transformed": transformed_df.head(10).round(4).to_dict(orient="records")
    }

if __name__ == "__main__":
    from ml.data_loader import load_raw_data, clean_and_standardize_data
    df = clean_and_standardize_data(load_raw_data())
    info = inspect_transformed_features(df)
    print("Features after encoding:", info["encoded_feature_names"])
    print("Sample:", info["sample_transformed"][:2])
