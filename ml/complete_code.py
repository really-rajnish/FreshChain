"""
================================================================================
 FRESHCHAIN - COMPLETE MACHINE LEARNING PIPELINE
 End-to-end data processing, exploratory analysis, scaling, outlier handling,
 regression modeling, and produce freshness classification with ensemble &
 gradient boosting models (AdaBoost, XGBoost, LightGBM).
================================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


# =========================================================
# 1. LOAD FRESHCHAIN DATA
# =========================================================

def load_data(filepath=None):
    """
    Loads and standardizes the FreshChain produce dataset (Dataset.csv).
    Handles relative paths, strips extra whitespace, and harmonizes class labels.
    """
    if filepath and os.path.exists(filepath):
        df = pd.read_csv(filepath)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        candidate_paths = [
            os.path.join(base_dir, "data", "Dataset.csv"),
            os.path.join(base_dir, "Dataset.csv"),
            os.path.join(curr_dir, "data", "Dataset.csv"),
            os.path.join(curr_dir, "Dataset.csv"),
            os.path.join("data", "Dataset.csv"),
            "Dataset.csv",
        ]
        found_path = None
        for path in candidate_paths:
            if os.path.exists(path):
                found_path = path
                break

        if not found_path:
            raise FileNotFoundError(
                "Could not find 'Dataset.csv'. Checked paths:\n"
                + "\n".join(candidate_paths)
            )
        df = pd.read_csv(found_path)

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Clean text columns
    if "Fruit" in df.columns:
        df["Fruit"] = df["Fruit"].astype(str).str.strip().str.capitalize()
    if "Class" in df.columns:
        # Harmonize 'Bad' and 'BAD' -> 'Bad', 'Good' -> 'Good'
        df["Class"] = df["Class"].astype(str).str.strip().str.capitalize()

    return df


# =========================================================
# 2. DATASET SUMMARY
# =========================================================

def summarize(df):
    """Prints comprehensive overview of the FreshChain dataset."""
    print("\n========== FRESHCHAIN DATA SUMMARY ==========")
    print("\n--- Shape ---")
    print(f"Total Produce Records: {df.shape[0]}, Total Features: {df.shape[1]}")

    print("\n--- First 5 Produce Samples ---")
    print(df.head())

    print("\n--- Produce Varieties (Fruit) ---")
    if "Fruit" in df.columns:
        print(df["Fruit"].value_counts())

    print("\n--- Freshness Status Distribution (Class) ---")
    if "Class" in df.columns:
        print(df["Class"].value_counts())

    print("\n--- Descriptive Statistics ---")
    print(df.describe())

    print("\n--- Missing Values Per Column ---")
    print(df.isnull().sum())


# =========================================================
# 3. STATISTICAL ANALYSIS
# =========================================================

def stat(df):
    """Computes mean, standard deviation, skewness, kurtosis, and correlation for sensor metrics."""
    print("\n========== SENSOR STATISTICAL ANALYSIS ==========")
    num_cols = df.select_dtypes(include=np.number)
    print("\nNumerical Sensor Features:")
    print(num_cols.columns.tolist())

    mean_values = num_cols.mean()
    print("\nMean Values:")
    print(mean_values)

    std_values = num_cols.std()
    print("\nStandard Deviation:")
    print(std_values)

    skewness = num_cols.skew()
    print("\nSkewness:")
    print(skewness)

    kurtosis = num_cols.kurt()
    print("\nKurtosis:")
    print(kurtosis)

    correlation = num_cols.corr()
    print("\nCorrelation Matrix:")
    print(correlation)

    return num_cols, mean_values, std_values, skewness, kurtosis, correlation


# =========================================================
# 4. DATA VISUALIZATION
# =========================================================

def visualize(df, save_dir=None):
    """Generates exploratory visualizations for environmental sensors and freshness quality."""
    numeric_df = df.select_dtypes(include=np.number)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # 1. Sensor correlation heatmap
    sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu", ax=axes[0, 0])
    axes[0, 0].set_title("Environmental Sensors Correlation Heatmap")

    # 2. Freshness quality distribution
    if "Class" in df.columns:
        sns.countplot(data=df, x="Class", ax=axes[0, 1], palette=["#10b981", "#ef4444"])
        axes[0, 1].set_title("Produce Quality Status (Class)")

    # 3. CO2 concentration boxplot
    if "CO2 (pmm)" in df.columns:
        sns.boxplot(y=df["CO2 (pmm)"], ax=axes[0, 2], color="#34d399")
        axes[0, 2].set_title("CO2 (pmm) Sensor Distribution")

    # 4. Storage temperature distribution
    if "Temp" in df.columns:
        sns.histplot(df["Temp"], kde=True, ax=axes[1, 0], color="#f97316")
        axes[1, 0].set_title("Temperature (°C) Distribution")

    # 5. Humidity boxplot
    if "Humid (%)" in df.columns:
        sns.boxplot(y=df["Humid (%)"], ax=axes[1, 1], color="#38bdf8")
        axes[1, 1].set_title("Humidity (%) Sensor Distribution")

    # 6. Storage Temperature vs CO2 scatterplot
    if "Temp" in df.columns and "CO2 (pmm)" in df.columns:
        sns.scatterplot(
            data=df,
            x="Temp",
            y="CO2 (pmm)",
            hue="Class" if "Class" in df.columns else None,
            palette=["#10b981", "#ef4444"],
            alpha=0.6,
            ax=axes[1, 2],
        )
        axes[1, 2].set_title("Temperature vs CO2 (pmm)")

    plt.tight_layout()

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        chart_path = os.path.join(save_dir, "freshchain_eda_overview.png")
        plt.savefig(chart_path, dpi=150)
        print(f"Visualizations saved to: {chart_path}")

    plt.show()


# =========================================================
# 5. FEATURE SCALING (NORMALIZATION & STANDARDIZATION)
# =========================================================

def normalize(df, exclude_cols=None):
    """
    Performs Min-Max Normalization and Z-Score Standardization
    on numerical sensor measurements while preserving categorical/target features.
    """
    print("\n========== FEATURE SCALING ==========")

    if exclude_cols is None:
        exclude_cols = ["Class", "Fruit"]

    numeric_cols_all = df.select_dtypes(include=np.number).columns
    scale_cols = [c for c in numeric_cols_all if c not in exclude_cols]

    numeric_df = df[scale_cols].copy()
    keep_df = df.drop(columns=scale_cols).copy()

    print("\nOriginal Produce Data Sample:")
    print(df.head())

    # Min-Max Normalization (Scales values into [0, 1])
    min_max_scaler = MinMaxScaler()
    normalized_array = min_max_scaler.fit_transform(numeric_df)
    normalized_numeric_df = pd.DataFrame(
        normalized_array, columns=numeric_df.columns, index=numeric_df.index
    )
    normalized_df = pd.concat([keep_df, normalized_numeric_df], axis=1)[df.columns]

    print("\n========== MIN-MAX NORMALIZED SENSOR DATA ==========")
    print(normalized_df.head())

    # Standardization (Zero mean, unit variance)
    standard_scaler = StandardScaler()
    standardized_array = standard_scaler.fit_transform(numeric_df)
    standardized_numeric_df = pd.DataFrame(
        standardized_array, columns=numeric_df.columns, index=numeric_df.index
    )
    standardized_df = pd.concat([keep_df, standardized_numeric_df], axis=1)[df.columns]

    print("\n========== STANDARDIZED SENSOR DATA ==========")
    print(standardized_df.head())

    return normalized_df, standardized_df


# =========================================================
# 6. SENSOR OUTLIER HANDLING (IQR CLIPPING)
# =========================================================

def outlier(df, col="CO2 (pmm)"):
    """
    Identifies and clips extreme sensor readings using Interquartile Range (IQR).
    Bounds: [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]
    """
    if col not in df.columns:
        print(f"Column '{col}' not found for outlier clipping.")
        return df

    df = df.copy()
    print(f"\n========== SENSOR OUTLIER HANDLING ({col}) ==========")
    print("\nBefore Clipping:")
    print(df[col].describe())

    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    df[col] = df[col].clip(lower=lower, upper=upper)

    print(f"\nIQR Bounds applied: Lower = {lower:.4f}, Upper = {upper:.4f}")
    print("\nAfter Clipping:")
    print(df[col].describe())

    return df


# =========================================================
# 7. ONE-HOT ENCODING
# =========================================================

def onehot(df):
    """
    Encodes nominal features (such as produce variety 'Fruit') using One-Hot Encoding.
    Fits strictly on train split to prevent data leakage.
    """
    nominal_cols = ["Fruit"]
    nominal_cols = [c for c in nominal_cols if c in df.columns]

    if not nominal_cols:
        print("No categorical columns available for one-hot encoding.")
        return None, None

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["Class"] if "Class" in df.columns else None
    )

    ohe = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    train_ohe = ohe.fit_transform(train_df[nominal_cols])
    test_ohe = ohe.transform(test_df[nominal_cols])
    ohe_cols = ohe.get_feature_names_out(nominal_cols)

    train_ohe_df = pd.DataFrame(train_ohe, columns=ohe_cols, index=train_df.index)
    test_ohe_df = pd.DataFrame(test_ohe, columns=ohe_cols, index=test_df.index)

    print("\n========== ONE-HOT ENCODED PRODUCE VARIETIES ==========")
    print("\nTraining Encoded Features:")
    print(train_ohe_df.head())
    print("\nTesting Encoded Features:")
    print(test_ohe_df.head())

    return train_ohe_df, test_ohe_df


# =========================================================
# 8. GRADIENT DESCENT (MANUAL IMPLEMENTATION)
# =========================================================

def gradient_descent(X, y, learning_rate=0.0001, iterations=1000):
    """
    Fits simple linear regression using manual Batch Gradient Descent.
    Computes MSE and parameter updates iteratively.
    """
    X = np.asarray(X, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    m = len(y)

    theta0 = 0.0  # Intercept
    theta1 = 0.0  # Slope
    mse_history = []

    for _ in range(iterations):
        y_pred = theta0 + theta1 * X
        error = y_pred - y
        mse = np.mean(error ** 2)
        mse_history.append(mse)

        d_theta0 = (2 / m) * np.sum(error)
        d_theta1 = (2 / m) * np.sum(error * X)

        theta0 = theta0 - learning_rate * d_theta0
        theta1 = theta1 - learning_rate * d_theta1

    return theta0, theta1, mse_history


# =========================================================
# 9. SIMPLE LINEAR REGRESSION VIA GRADIENT DESCENT
# =========================================================

def simple_linear_regression_GD(df, feature="Temp", target="CO2 (pmm)"):
    """
    Predicts environmental target (e.g., CO2 level) from sensor feature (e.g., Temperature)
    using manual Gradient Descent.
    """
    print("\n========== LINEAR REGRESSION (GRADIENT DESCENT) ==========")
    if feature not in df.columns or target not in df.columns:
        raise ValueError(f"Required columns '{feature}' or '{target}' not found in dataset.")

    X = df[[feature]]
    y = df[target]

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)
    theta0, theta1, mse_history = gradient_descent(train_X, train_y, learning_rate=0.0001, iterations=1000)

    print(f"\nFeature: {feature} -> Target: {target}")
    print("Theta0 (Intercept):", theta0)
    print("Theta1 (Slope):", theta1)

    test_X_array = test_X[feature].values
    y_pred = theta0 + theta1 * test_X_array

    mse1 = mean_squared_error(test_y, y_pred)
    rsq1 = r2_score(test_y, y_pred)

    print("Test MSE:", mse1)
    print("R-Squared Score:", rsq1)

    return theta0, theta1, mse1, rsq1


# =========================================================
# 10. SCIKIT-LEARN LINEAR, LASSO, & RIDGE REGRESSION
# =========================================================

def simple_linear_regression(df, feature="Temp", target="CO2 (pmm)"):
    """
    Benchmarks Linear Regression, Lasso (L1 Regularization),
    and Ridge (L2 Regularization) for predicting CO2 from Temperature.
    """
    print("\n========== SKLEARN REGRESSION BENCHMARK ==========")
    if feature not in df.columns or target not in df.columns:
        raise ValueError(f"Required columns '{feature}' or '{target}' not found in dataset.")

    X = df[[feature]]
    y = df[target]

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)

    ols = LinearRegression()
    lasso = Lasso(alpha=0.1)
    ridge = Ridge(alpha=0.1)

    ols.fit(train_X, train_y)
    lasso.fit(train_X, train_y)
    ridge.fit(train_X, train_y)

    y_pred_ols = ols.predict(test_X)
    y_pred_lasso = lasso.predict(test_X)
    y_pred_ridge = ridge.predict(test_X)

    mse_ols = mean_squared_error(test_y, y_pred_ols)
    mse_lasso = mean_squared_error(test_y, y_pred_lasso)
    mse_ridge = mean_squared_error(test_y, y_pred_ridge)
    rsq = r2_score(test_y, y_pred_ols)

    print(f"Feature: {feature} -> Target: {target}")
    print("OLS Intercept:", ols.intercept_)
    print("OLS Coefficient:", ols.coef_[0])
    print("OLS Linear Regression MSE:", mse_ols)
    print("Lasso Regression MSE:       ", mse_lasso)
    print("Ridge Regression MSE:       ", mse_ridge)
    print("R-Squared Score:            ", rsq)

    return ols


# =========================================================
# 11. LOGISTIC REGRESSION (FRESHNESS CLASSIFICATION)
# =========================================================

def simple_logistic_regression(df):
    """
    Predicts produce freshness status ('Good' vs 'Bad') from environmental sensor features
    using Logistic Regression. Evaluates Accuracy, Confusion Matrix, and class probabilities.
    """
    print("\n========== LOGISTIC REGRESSION FRESHNESS CLASSIFICATION ==========")
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    y = df[target]

    train_X, test_X, train_y, test_y = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(train_X, train_y)

    print("Classes:", model.classes_)
    print("Intercept:", model.intercept_)
    print("Coefficients:", dict(zip(features, model.coef_[0])))

    y_pred = model.predict(test_X)
    accuracy = accuracy_score(test_y, y_pred)
    print(f"Logistic Regression Accuracy: {accuracy:.4f}")

    cm = confusion_matrix(test_y, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    # Sample predictions
    y_prob = model.predict_proba(test_X)[:, 1]
    print("\nSample Produce Freshness Predictions:")
    for i in range(min(5, len(test_X))):
        print(
            f"Produce Sample {test_X.index[i]}: "
            f"Temp={test_X.iloc[i]['Temp']:.1f}, CO2={test_X.iloc[i]['CO2 (pmm)']:.1f} "
            f"| Actual: {test_y.iloc[i]:<4} "
            f"| Probability: {y_prob[i]:.4f} "
            f"| Prediction: {y_pred[i]}"
        )

    return model


# =========================================================
# 12. DECISION TREE CLASSIFIER
# =========================================================

def decision_tree(df):
    """Trains an unpruned Decision Tree Classifier for Produce Freshness classification."""
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)

    y_pred = dt.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Decision Tree Accuracy:        {acc:.4f}")

    return dt


# =========================================================
# 13. PRUNED DECISION TREE
# =========================================================

def decision_tree_pruned(df):
    """
    Trains a regularized/pruned Decision Tree Classifier with depth and leaf constraints
    to mitigate overfitting and improve generalization on fresh produce data.
    """
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=4,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Pruned Decision Tree Accuracy: {acc:.4f}")

    return model


# =========================================================
# 14. RANDOM FOREST CLASSIFIER
# =========================================================

def random_forest_model(df):
    """Trains an Ensemble Random Forest Classifier with 100 decision trees."""
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(
        n_estimators=100,
        criterion="gini",
        max_depth=5,
        random_state=42,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Random Forest Accuracy:        {acc:.4f}")

    return rf


# =========================================================
# 15. ADABOOST CLASSIFIER
# =========================================================

def adaboost_model(df):
    """
    Trains an AdaBoost (Adaptive Boosting) Classifier.
    Sequentially fits weak decision stumps, placing higher weights on misclassified samples.
    """
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    ada = AdaBoostClassifier(n_estimators=100, random_state=42)
    ada.fit(X_train, y_train)

    y_pred = ada.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"AdaBoost Accuracy:             {acc:.4f}")

    return ada


# =========================================================
# 16. XGBOOST CLASSIFIER
# =========================================================

def xgboost_model(df):
    """
    Trains an XGBoost (Extreme Gradient Boosting) Classifier.
    Uses second-order Taylor expansion for loss optimization, shrinkage, and tree pruning.
    """
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    le = LabelEncoder()
    y = le.fit_transform(df[target])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    xgb = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
    )
    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"XGBoost Accuracy:              {acc:.4f}")

    return xgb, le


# =========================================================
# 17. LIGHTGBM CLASSIFIER
# =========================================================

def lightgbm_model(df):
    """
    Trains a LightGBM (Light Gradient Boosting Machine) Classifier.
    Uses histogram-based algorithms and leaf-wise (best-first) tree growth for high efficiency.
    """
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in df.columns]
    target = "Class"

    X = df[features]
    le = LabelEncoder()
    y = le.fit_transform(df[target])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    lgb = LGBMClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        verbose=-1,
    )
    lgb.fit(X_train, y_train)

    y_pred = lgb.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"LightGBM Accuracy:             {acc:.4f}")

    return lgb, le


# =========================================================
# 18. MULTI-MODEL PREDICTION COMPARISON
# =========================================================

def compare(sample_df, m1, m2, m3, m4, m5_tuple, m6_tuple):
    """
    Compares predictions across all 6 models:
    - Decision Tree
    - Pruned Decision Tree
    - Random Forest
    - AdaBoost
    - XGBoost
    - LightGBM
    against the actual ground truth produce quality labels.
    """
    features = [c for c in ["Temp", "Humid (%)", "Light (Fux)", "CO2 (pmm)"] if c in sample_df.columns]
    target = "Class"

    X_sample = sample_df[features]
    y_actual = sample_df[target]

    pred_dt = m1.predict(X_sample)
    pred_pruned = m2.predict(X_sample)
    pred_rf = m3.predict(X_sample)
    pred_ada = m4.predict(X_sample)

    m5_xgb, le_xgb = m5_tuple
    pred_xgb = le_xgb.inverse_transform(m5_xgb.predict(X_sample))

    m6_lgb, le_lgb = m6_tuple
    pred_lgb = le_lgb.inverse_transform(m6_lgb.predict(X_sample))

    results = pd.DataFrame({
        "SampleID": sample_df.index,
        "Fruit": sample_df["Fruit"] if "Fruit" in sample_df.columns else "-",
        "Actual Quality": y_actual.values,
        "Decision Tree": pred_dt,
        "Pruned Tree": pred_pruned,
        "Random Forest": pred_rf,
        "AdaBoost": pred_ada,
        "XGBoost": pred_xgb,
        "LightGBM": pred_lgb,
    })

    print("\n" + "=" * 115)
    print(" FRESHCHAIN: COMPREHENSIVE MULTI-MODEL PREDICTION BENCHMARK FOR 10 SAMPLES")
    print("=" * 115)
    print(results.to_string(index=False))


# =========================================================
# MAIN EXECUTION PIPELINE
# =========================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" FRESHCHAIN AUTOMATED MACHINE LEARNING PIPELINE")
    print("=" * 75)

    # 1. Load Dataset
    df = load_data()
    print("Dataset Shape:", df.shape)
    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nProduce Freshness (Class) Counts:")
    print(df["Class"].value_counts())

    # Optional Exploratory / Statistical Analysis (uncomment when required):
    # summarize(df)
    # stat(df)
    # visualize(df)

    # 2. Scaling (Min-Max and Standardization)
    normalized_df, standardized_df = normalize(df, exclude_cols=["Class", "Fruit"])

    # 3. Outlier Handling on Sensor Readings
    standardized_df = outlier(standardized_df, col="CO2 (pmm)")

    # 4. Optional One-Hot Encoding & Linear/Logistic Regression demos
    # train_ohe, test_ohe = onehot(standardized_df)
    # simple_linear_regression(standardized_df)
    # simple_linear_regression_GD(standardized_df)
    # simple_logistic_regression(standardized_df)

    # 5. Train Freshness Classification Models
    print("\n========== TRAINING FRESHCHAIN CLASSIFIERS ==========")
    m1 = decision_tree(standardized_df)
    m2 = decision_tree_pruned(standardized_df)
    m3 = random_forest_model(standardized_df)
    m4 = adaboost_model(standardized_df)
    m5 = xgboost_model(standardized_df)
    m6 = lightgbm_model(standardized_df)

    # 6. Prediction Comparison on 10 Produce Samples
    sample_df = standardized_df.sample(n=10, random_state=42)
    compare(sample_df, m1, m2, m3, m4, m5, m6)
