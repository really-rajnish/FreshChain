import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import pandas as pd

from ml.data_loader import load_raw_data, clean_and_standardize_data, get_data_summary
from ml.eda import generate_all_eda_charts, get_eda_insights
from ml.feature_engg import inspect_transformed_features
from ml.trainer import train_and_evaluate_models
from models.load import load_trained_model, predict_freshness

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "freshchain-secret-key-2026")

@app.route("/")
def index():
    try:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        summary = get_data_summary(df)
    except Exception as e:
        summary = None
        
    try:
        model_bundle = load_trained_model()
    except Exception:
        model_bundle = None
        
    return render_template("index.html", summary=summary, model_info=model_bundle)

@app.route("/data")
def data_page():
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    summary = get_data_summary(df)
    return render_template("data_loading.html", summary=summary)

@app.route("/eda")
def eda_page():
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    
    # Ensure charts exist
    charts_dir = os.path.join(app.root_path, "static", "charts")
    if not os.path.exists(os.path.join(charts_dir, "class_distribution.png")):
        generate_all_eda_charts(df)
        
    insights = get_eda_insights(df)
    return render_template("eda.html", insights=insights)

@app.route("/eda/regenerate", methods=["POST"])
def regenerate_eda():
    try:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        generate_all_eda_charts(df)
        flash("EDA visual charts regenerated successfully!", "success")
    except Exception as e:
        flash(f"Error generating charts: {str(e)}", "danger")
    return redirect(url_for("eda_page"))

@app.route("/feature-engg")
def feature_engg_page():
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    feature_info = inspect_transformed_features(df)
    return render_template("feature_engg.html", feature_info=feature_info)

@app.route("/train")
def train_page():
    bundle = load_trained_model()
    return render_template("train.html", model_bundle=bundle)

@app.route("/train/run", methods=["POST"])
def retrain_model():
    try:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        results = train_and_evaluate_models(df)
        load_trained_model(force_reload=True)
        flash(f"Training complete! Best Model: {results['best_model']} with {results['best_metrics']['accuracy']*100:.2f}% accuracy.", "success")
    except Exception as e:
        flash(f"Training failed: {str(e)}", "danger")
    return redirect(url_for("train_page"))

@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    try:
        raw = load_raw_data()
        df = clean_and_standardize_data(raw)
        fruits = sorted(df["Fruit"].unique().tolist())
    except Exception:
        fruits = ["Banana", "Orange", "Pineapple", "Tomato"]
        
    result = None
    if request.method == "POST":
        try:
            fruit = request.form.get("fruit", "Orange")
            temp = float(request.form.get("temp", 22.0))
            humid = float(request.form.get("humid", 95.0))
            light = float(request.form.get("light", 7.35))
            co2 = float(request.form.get("co2", 360.0))
            
            result = predict_freshness(fruit, temp, humid, light, co2)
        except Exception as e:
            flash(f"Prediction error: {str(e)}", "danger")
            
    return render_template("predict.html", fruits=fruits, result=result)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True, silent=True) or {}
    fruit = data.get("fruit", "Orange")
    temp = float(data.get("temp", 22.0))
    humid = float(data.get("humid", 95.0))
    light = float(data.get("light", 7.35))
    co2 = float(data.get("co2", 360.0))
    
    try:
        res = predict_freshness(fruit, temp, humid, light, co2)
        return jsonify({"status": "success", "data": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/presentation")
def presentation_page():
    return render_template("presentation.html")

@app.route("/download-pptx")
def download_pptx():
    pptx_path = os.path.join(app.root_path, "FreshChain_Presentation.pptx")
    if not os.path.exists(pptx_path):
        from generate_presentation import create_presentation
        create_presentation()
    return send_file(pptx_path, as_attachment=True, download_name="FreshChain_Presentation.pptx")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
