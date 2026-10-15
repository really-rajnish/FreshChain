import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from ml.data_loader import load_raw_data, clean_and_standardize_data
from ml.feature_engg import build_preprocessor, get_train_test_data

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")

def get_model_save_path() -> str:
    os.makedirs(MODELS_DIR, exist_ok=True)
    return os.path.join(MODELS_DIR, "freshchain_model.joblib")

def train_and_evaluate_models(df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Trains multiple classifier models, evaluates metrics, selects the best model,
    and saves the full pipeline to disk.
    """
    if df is None:
        raw_df = load_raw_data()
        df = clean_and_standardize_data(raw_df)
        
    X_train, X_test, y_train, y_test = get_train_test_data(df)
    preprocessor = build_preprocessor()
    
    candidate_models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = {}
    best_name = None
    best_f1 = -1.0
    best_pipeline = None
    
    for name, clf in candidate_models.items():
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        # Calculate probabilities if available
        if hasattr(pipeline, "predict_proba"):
            y_proba = pipeline.predict_proba(X_test)[:, 1]
            auc = round(float(roc_auc_score(y_test, y_proba)), 4)
        else:
            auc = None
            
        acc = round(float(accuracy_score(y_test, y_pred)), 4)
        prec = round(float(precision_score(y_test, y_pred, zero_division=0)), 4)
        rec = round(float(recall_score(y_test, y_pred, zero_division=0)), 4)
        f1 = round(float(f1_score(y_test, y_pred, zero_division=0)), 4)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": auc,
            "confusion_matrix": cm,
            "test_samples": len(y_test)
        }
        
        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_pipeline = pipeline
            
    # Save best pipeline
    save_path = get_model_save_path()
    joblib.dump({
        "pipeline": best_pipeline,
        "best_model_name": best_name,
        "metrics": results[best_name],
        "all_results": results,
        "fruits": sorted(df["Fruit"].unique().tolist()) if "Fruit" in df.columns else []
    }, save_path)
    
    return {
        "best_model": best_name,
        "best_metrics": results[best_name],
        "all_results": results,
        "model_file": save_path
    }

if __name__ == "__main__":
    out = train_and_evaluate_models()
    print("Training finished!")
    print("Best Model:", out["best_model"])
    print("Best Metrics:", out["best_metrics"])
