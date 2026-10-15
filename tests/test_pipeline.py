import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.data_loader import load_raw_data, clean_and_standardize_data, get_data_summary
from ml.feature_engg import build_preprocessor, prepare_features_and_target, get_train_test_data
from ml.trainer import train_and_evaluate_models
from models.load import load_trained_model, predict_freshness

def test_data_loader():
    df = load_raw_data()
    assert not df.empty
    assert "Fruit" in df.columns
    assert "Class" in df.columns
    
    cleaned = clean_and_standardize_data(df)
    assert not cleaned.empty
    assert set(cleaned["Class"].unique()).issubset({"Good", "Bad"})
    
    summary = get_data_summary(cleaned)
    assert summary["num_rows"] > 0
    assert "Orange" in summary["fruits"]

def test_feature_engineering():
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    X, y = prepare_features_and_target(df)
    assert len(X) == len(y)
    
    X_train, X_test, y_train, y_test = get_train_test_data(df, test_size=0.2)
    assert len(X_train) > 0
    assert len(X_test) > 0

def test_model_training_and_inference():
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    results = train_and_evaluate_models(df)
    
    assert "best_model" in results
    assert results["best_metrics"]["accuracy"] > 0.85
    
    # Test Prediction helper
    pred_good = predict_freshness("Orange", 22.0, 95.0, 7.35, 361.0)
    assert pred_good["quality_prediction"] in ["Good", "Bad"]
    assert "confidence_score" in pred_good
    assert "probability_good" in pred_good

if __name__ == "__main__":
    print("Running tests...")
    test_data_loader()
    print("[PASS] test_data_loader")
    test_feature_engineering()
    print("[PASS] test_feature_engineering")
    test_model_training_and_inference()
    print("[PASS] test_model_training_and_inference")
    print("\nALL TESTS PASSED SUCCESSFULLY! (3/3)")

