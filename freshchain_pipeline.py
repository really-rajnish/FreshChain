"""
FreshChain / Placement Pipeline Runner
Command-line interface to orchestrate Data Loading, EDA Chart Generation, Feature Engineering, and Model Training.
"""

import sys
import argparse
from ml.data_loader import load_raw_data, clean_and_standardize_data, get_data_summary
from ml.eda import generate_all_eda_charts, get_eda_insights
from ml.feature_engg import inspect_transformed_features
from ml.trainer import train_and_evaluate_models

def run_pipeline():
    print("=" * 65)
    print(" FRESHCHAIN AUTOMATED ML PIPELINE")
    print("=" * 65)
    
    # 1. Load Data
    print("\n[STEP 1/4] Loading and cleaning dataset...")
    raw = load_raw_data()
    df = clean_and_standardize_data(raw)
    summary = get_data_summary(df)
    print(f" -> Processed {summary['num_rows']} rows across {summary['num_columns']} columns.")
    print(f" -> Unique produce varieties: {', '.join(summary['fruits'])}")
    print(f" -> Class distribution: {summary['classes']}")
    
    # 2. EDA
    print("\n[STEP 2/4] Generating exploratory data visualization charts...")
    charts = generate_all_eda_charts(df)
    print(f" -> Saved {len(charts)} charts to static/charts/: {', '.join(charts)}")
    
    # 3. Feature Engineering
    print("\n[STEP 3/4] Validating feature transformations...")
    ft = inspect_transformed_features(df)
    print(f" -> Features transformed: {ft['num_features_before']} raw -> {ft['num_features_after']} encoded")
    print(f" -> Features: {ft['encoded_feature_names']}")
    
    # 4. Model Training
    print("\n[STEP 4/4] Training and benchmarking candidate ML models...")
    train_results = train_and_evaluate_models(df)
    print(f" -> Winning Model: {train_results['best_model']}")
    print(f" -> Metrics: Accuracy={train_results['best_metrics']['accuracy']:.4f}, F1={train_results['best_metrics']['f1_score']:.4f}, AUC={train_results['best_metrics']['roc_auc']:.4f}")
    print(f" -> Model artifact saved to: {train_results['model_file']}")
    print("\n" + "=" * 65)
    print(" Pipeline completed successfully!")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline()
