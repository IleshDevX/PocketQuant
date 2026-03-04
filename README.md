# PocketQuant — Merchant Liquidity Shortage Prediction

PocketQuant is an end-to-end ML system for predicting whether a merchant will face a liquidity shortage in the next 48 hours (`liquidity_shortage_next_48h`).

It includes:
- data validation + EDA + feature engineering notebooks,
- model training/evaluation/explainability outputs,
- a production-style FastAPI prediction service,
- and a Streamlit risk intelligence dashboard.

---

## 1) Project Insights (from current artifacts)

### Data insights
- **Rows:** 50,000 merchant-day records
- **Raw columns:** 59
- **Unique merchants:** 1,000
- **Date range:** 2024-01-01 to 2024-06-28
- **Target positives:** 645 / 50,000
- **Shortage rate:** **1.29%**
- **Class imbalance:** **76.52:1** (negative:positive)

### Modeling insights
From `models/artifacts/model_metrics.csv`:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9929 | 0.6726 | 0.8760 | 0.7609 | 0.9976 |
| Random Forest | 0.9945 | 0.7102 | 0.9690 | 0.8197 | 0.9988 |
| XGBoost | 0.9954 | 0.7677 | 0.9225 | 0.8380 | 0.9992 |
| **XGBoost (Tuned)** | **0.9956** | **0.7778** | **0.9225** | **0.8440** | **0.9991** |

### Threshold strategy insight
From `models/artifacts/threshold_analysis.csv`:
- **Best F1 around threshold 0.60** (`F1 ≈ 0.8530`, `Precision ≈ 0.7933`, `Recall ≈ 0.9225`)
- **Operational threshold 0.40** (used in API startup) gives:
  - Precision: `0.7547`
  - Recall: `0.9302`
  - F1: `0.8333`

This is aligned with risk operations where missing true shortages is costly.

### Explainability + fairness insight
From `reports/explainability_report.txt` and explainability artifacts:
- Most influential feature: **`liquidity_buffer_ratio`**
  - Native importance: `0.6853`
  - SHAP importance: `8.4543`
- Feature category contribution:
  - **Liquidity Health:** `0.7860` (dominant)
  - Merchant Profile: `0.0694`
  - Transaction Metrics: `0.0560`
- Bias check by merchant category:
  - Recall variance: `0.0189`
  - Precision variance: `0.0506`
  - Report status: **No significant bias detected**

---

## 2) Repository Structure

```text
PocketQuant/
├─ configs/
│  └─ config.yaml
├─ data/
│  ├─ merchant_liquidity.csv
│  └─ processed/
│     ├─ merchant_liquidity_validated.csv
│     ├─ merchant_liquidity_engineered.csv
│     ├─ feature_matrix_X.csv
│     ├─ target_y.csv
│     └─ feature_list.txt
├─ models/
│  ├─ trained/
│  │  ├─ xgboost_liquidity_model.pkl
│  │  ├─ xgboost_liquidity_model.joblib
│  │  ├─ random_forest_model.pkl
│  │  ├─ logistic_regression_model.pkl
│  │  └─ ...
│  └─ artifacts/
│     ├─ model_metrics.csv
│     ├─ best_hyperparameters.csv
│     ├─ feature_importance.csv
│     ├─ feature_importance_detailed.csv
│     ├─ shap_feature_importance.csv
│     ├─ threshold_analysis.csv
│     └─ bias_analysis.csv
├─ notebooks/
│  ├─ 01_data_audit_validation.ipynb
│  ├─ 02_Exploratory_Data_Analysis.ipynb
│  ├─ 03_Feature_Engineering.ipynb
│  ├─ 04_Model_Training.ipynb
│  └─ 05_Model_Explainability.ipynb
├─ reports/
│  ├─ eda_summary.txt
│  ├─ explainability_report.txt
│  └─ figures/
├─ src/
│  ├─ api/
│  │  ├─ main.py
│  │  ├─ predict.py
│  │  ├─ schemas.py
│  │  └─ logger.py
│  └─ dashboard/
│     ├─ app.py
│     ├─ api_client.py
│     └─ config.py
├─ tests/
│  └─ test_api.py
└─ requirements.txt
```

---

## 3) End-to-End Workflow

The project follows this phase sequence:

1. **Data Audit & Validation** (`notebooks/01_data_audit_validation.ipynb`)
    - integrity checks, missingness, duplicates, consistency, summary stats.
2. **EDA** (`notebooks/02_Exploratory_Data_Analysis.ipynb`)
    - target imbalance analysis, correlations, volatility/risk patterns.
3. **Feature Engineering** (`notebooks/03_Feature_Engineering.ipynb`)
    - rolling metrics recalculation, derived risk signals, encoding, final `X`/`y`.
4. **Model Training** (`notebooks/04_Model_Training.ipynb`)
    - stratified split, imbalance handling, baseline vs tuned models.
5. **Explainability & Validation** (`notebooks/05_Model_Explainability.ipynb`)
    - feature importance, SHAP, threshold sensitivity, category bias checks.

---

## 4) API Service (FastAPI)

Core file: `src/api/main.py`

### Features
- Loads global predictor at startup (`threshold=0.40`)
- Single and batch predictions
- Typed request/response via Pydantic schemas
- Request ID + processing-time middleware
- Structured prediction/error logging in `logs/`

### Endpoints
- `GET /` — service info
- `GET /health` — health + model-loaded status
- `POST /predict-risk` — single merchant scoring
- `POST /predict-risk/batch` — batch scoring (up to 100)
- `GET /model/info` — model metadata + top features + performance snapshot

### Run API
```bash
uvicorn src.api.main:app --reload
```

Docs available at:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

---

## 5) Dashboard (Streamlit)

Core file: `src/dashboard/app.py`

### What it provides
- Merchant multi-select and comparison table
- Real-time API health/status banner
- KPI cards (inflow, net cash flow, buffer days, credit utilization)
- Risk panel with probability + threshold + action context
- Contributing risk factors
- Analytics charts:
  - 7-day cashflow trend (inflow/outflow/net)
  - radar-based financial health profile
- Detailed tabs: Liquidity Metrics, Risk Indicators, Merchant Profile

### Runtime behavior insight
- Dashboard contains a synthetic merchant generator (`SAMPLE_MERCHANTS`) for interactive demo.
- If API is unreachable, it falls back to heuristic risk estimation so UI remains usable.

### Run dashboard
```bash
streamlit run src/dashboard/app.py --server.port 8505
```

---

## 6) Setup Instructions

### Prerequisites
- Python 3.9+
- pip

### Install
```bash
git clone <your-repo-url>
cd PocketQuant

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate

pip install -r requirements.txt
```

### Important dependency note
The current `requirements.txt` is strong for notebook/ML workflow, but API/dashboard runtime packages are not listed there yet.

Install these for full app execution:
```bash
pip install fastapi uvicorn streamlit requests shap
```

---

## 7) How to Use

### Option A: API only
1. Start API:
    ```bash
    uvicorn src.api.main:app --reload
    ```
2. Open interactive docs: `http://localhost:8000/docs`

### Option B: API + Dashboard
1. Start API (`localhost:8000`)
2. In another terminal, start dashboard:
    ```bash
    streamlit run src/dashboard/app.py --server.port 8505
    ```
3. Open dashboard URL printed by Streamlit.

### Option C: quick endpoint smoke test
```bash
python tests/test_api.py
```

---

## 8) Key Artifacts You Can Reuse

- **Best model:** `models/trained/xgboost_liquidity_model.pkl`
- **Model comparison:** `models/artifacts/model_metrics.csv`
- **Best hyperparameters:** `models/artifacts/best_hyperparameters.csv`
- **Feature importance:**
  - `models/artifacts/feature_importance.csv`
  - `models/artifacts/feature_importance_detailed.csv`
- **SHAP importance:** `models/artifacts/shap_feature_importance.csv`
- **Threshold operating analysis:** `models/artifacts/threshold_analysis.csv`
- **Bias analysis:** `models/artifacts/bias_analysis.csv`
- **EDA summary:** `reports/eda_summary.txt`
- **Explainability report:** `reports/explainability_report.txt`

---

## 9) Observations and Recommendations

1. **Excellent ranking performance** (ROC-AUC ~0.999), but this level warrants ongoing leakage/temporal robustness checks before production scaling.
2. **Operational threshold design is sensible** for risk management (0.40 prioritizes recall).
3. **Liquidity indicators dominate model decisions**, which matches financial intuition and improves explainability credibility.
4. **Bias results are promising**, but fairness checks should be extended to additional slices (city/state/merchant age bands).
5. **Engineering next step:** align `requirements.txt` with deployable API/dashboard stack to simplify onboarding.

---

## 10) Current Project Status

- ✅ Data audit, EDA, feature engineering, training, and explainability phases implemented
- ✅ Trained models and evaluation artifacts available
- ✅ FastAPI prediction service implemented
- ✅ Streamlit intelligence dashboard implemented
- ⚠️ Dependency manifest needs API/dashboard additions for one-command setup

---

## 11) Notes for GitHub Publishing

Before publishing, recommended housekeeping:
- add a `LICENSE` file,
- add CI for API tests and linting,
- include deployment instructions (Docker/Cloud Run/Render/etc.),
- add sample request/response JSON snippets in API section.

---

If you want, I can also generate:
1) a production-ready `requirements-api.txt` or unified dependency file, and
2) a short `CONTRIBUTING.md` + `LICENSE` starter template.
