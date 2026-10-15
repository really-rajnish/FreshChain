# FreshChain 🌿

> **Intelligent Cold Chain & Freshness Prediction System**  
> Real-time shelf-life and produce quality prediction powered by environmental IoT telemetry (Temperature, Humidity, Light, CO₂) and Machine Learning.

---

## 📌 Overview

**FreshChain** is an end-to-end AgriTech platform designed to monitor environmental transit conditions for perishable produce (Banana, Orange, Pineapple, Tomato). By analyzing sensory data against trained ensemble and gradient-boosted models, FreshChain accurately flags suboptimal storage conditions and predicts produce status (`Good` vs `Bad`) before spoilage occurs.

---

## ✨ Features

- **Automated ML Pipeline**: Complete pipeline orchestrating data loading, label standardization, exploratory analysis, feature scaling, and multi-model benchmarking.
- **Ensemble & Boosting Classifiers**: Benchmarking across Random Forest, Gradient Boosting, AdaBoost, XGBoost, LightGBM, and Logistic Regression with automated hyperparameter evaluation.
- **Interactive Flask Dashboard**:
  - **Overview**: System metrics and dataset statistics.
  - **Data Explorer**: Dataset profiling and preview.
  - **Visual EDA**: High-resolution dark-mode distribution charts.
  - **Feature Inspector**: Standardized and one-hot encoded representations.
  - **Live Training**: Retrain and benchmark models directly from the GUI.
  - **Interactive Predictor**: Manual sensory input testing with instant confidence scores.
- **IoT REST API**: `POST /api/predict` endpoint for automated cold-chain telemetry ingestion.
- **Executive Pitch Decks**: Interactive HTML presentation deck and downloadable 12-slide PowerPoint presentation (`FreshChain_Presentation.pptx`).

---

## 📁 Repository Structure

```
FreshChain/
├── app.py                         # Flask web application & REST API
├── freshchain_pipeline.py         # 4-stage CLI orchestration runner
├── complete_code.py               # Comprehensive end-to-end ML pipeline script
├── generate_presentation.py       # Programmatic PowerPoint (.pptx) generator
├── presentation.html              # Interactive browser presentation deck
├── Dataset.csv                    # Primary produce sensor dataset (10,996 records)
├── requirements.txt               # Python package dependencies
│
├── ml/                            # Machine learning modules
│   ├── data_loader.py             # Data ingestion, cleaning, & label normalization
│   ├── eda.py                     # Visual data chart generator
│   ├── feature_engg.py            # Preprocessor (StandardScaler + OneHotEncoder)
│   └── trainer.py                 # Multi-model benchmarking & serialization
│
├── models/                        # Serialized ML pipeline artifacts
│   ├── freshchain_model.joblib    # Best-performing trained model bundle
│   └── load.py                    # Cached inference scoring engine
│
├── templates/                     # Flask Jinja2 UI templates
├── static/                        # CSS styles and generated charts
├── tests/                         # Unit tests
└── notebooks/                     # Exploratory scripts
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/really-rajnish/FreshChain.git
cd FreshChain
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Automated Pipeline
```bash
python freshchain_pipeline.py
```

### 4. Launch the Web Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## 🔌 REST API Documentation

### **Predict Freshness**
- **Endpoint**: `POST /api/predict`
- **Content-Type**: `application/json`

#### **Request Body**
```json
{
  "fruit": "Orange",
  "temp": 22.0,
  "humid": 95.0,
  "light": 7.35,
  "co2": 361.0
}
```

#### **Response Body**
```json
{
  "status": "success",
  "data": {
    "fruit": "Orange",
    "quality_prediction": "Good",
    "is_good": true,
    "confidence_score": 98.4,
    "probability_good": 98.4,
    "probability_bad": 1.6,
    "model_used": "Random Forest",
    "recommendation": "Optimal conditions maintained! Produce is fresh and fit for supply chain transit."
  }
}
```

---

## 🧪 Testing

Run the test suite to verify pipeline and model inference integrity:
```bash
python tests/test_pipeline.py
```

---

## 📄 License
This project is licensed under the MIT License.
