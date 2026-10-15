import os
import joblib
import pandas as pd
from typing import Dict, Any, Union, List

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(MODELS_DIR, "freshchain_model.joblib")
FALLBACK_MODEL_PATH = os.path.join(MODELS_DIR, "placement_model.joblib")

_CACHED_MODEL_BUNDLE = None

def get_model_path() -> str:
    if os.path.exists(DEFAULT_MODEL_PATH):
        return DEFAULT_MODEL_PATH
    if os.path.exists(FALLBACK_MODEL_PATH):
        return FALLBACK_MODEL_PATH
    return DEFAULT_MODEL_PATH

def load_trained_model(force_reload: bool = False) -> Dict[str, Any]:
    """Loads and caches the trained model bundle."""
    global _CACHED_MODEL_BUNDLE
    if _CACHED_MODEL_BUNDLE is not None and not force_reload:
        return _CACHED_MODEL_BUNDLE
        
    model_path = get_model_path()
    if not os.path.exists(model_path):
        from ml.trainer import train_and_evaluate_models
        train_and_evaluate_models()
        
    _CACHED_MODEL_BUNDLE = joblib.load(model_path)
    return _CACHED_MODEL_BUNDLE

def predict_freshness(
    fruit: str, 
    temp: float, 
    humid: float, 
    light: float, 
    co2: float
) -> Dict[str, Any]:
    """
    Makes a freshness quality prediction for single environmental condition entry.
    """
    bundle = load_trained_model()
    pipeline = bundle["pipeline"]
    
    input_df = pd.DataFrame([{
        "Fruit": str(fruit).strip().capitalize(),
        "Temp": float(temp),
        "Humid (%)": float(humid),
        "Light (Fux)": float(light),
        "CO2 (pmm)": float(co2)
    }])
    
    prediction_raw = pipeline.predict(input_df)[0]
    
    proba_good = None
    proba_bad = None
    confidence = None
    
    if hasattr(pipeline, "predict_proba"):
        probas = pipeline.predict_proba(input_df)[0]
        # Class 0 is Bad, Class 1 is Good
        proba_bad = round(float(probas[0]) * 100, 2)
        proba_good = round(float(probas[1]) * 100, 2)
        confidence = proba_good if prediction_raw == 1 else proba_bad
        
    quality_label = "Good" if prediction_raw == 1 else "Bad"
    
    status_color = "#10b981" if quality_label == "Good" else "#ef4444"
    status_icon = "check-circle" if quality_label == "Good" else "alert-triangle"
    recommendation = (
        "Optimal conditions maintained! Produce is fresh and fit for supply chain transit."
        if quality_label == "Good"
        else "Suboptimal environment! Immediate atmospheric or temperature adjustment recommended."
    )
    
    return {
        "fruit": fruit,
        "input_features": {
            "Temperature (°C)": temp,
            "Humidity (%)": humid,
            "Light Level (Fux)": light,
            "CO2 Level (ppm)": co2
        },
        "quality_prediction": quality_label,
        "is_good": bool(prediction_raw == 1),
        "confidence_score": confidence,
        "probability_good": proba_good,
        "probability_bad": proba_bad,
        "recommendation": recommendation,
        "status_color": status_color,
        "status_icon": status_icon,
        "model_used": bundle.get("best_model_name", "Random Forest")
    }

if __name__ == "__main__":
    res = predict_freshness("Orange", 22.0, 95.0, 7.35, 361.0)
    print("Prediction result:", res)
