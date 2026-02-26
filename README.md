# PocketQuant - Merchant Liquidity Shortage Prediction

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

PocketQuant is a machine learning system designed to predict merchant liquidity shortages within a 48-hour window. This enables proactive risk management and timely interventions for merchants on payment platforms.

## 📋 Business Objective

**Predict `liquidity_shortage_next_48h`** - A binary classification task to identify merchants at risk of facing liquidity challenges.

## 🏗️ Project Structure

```
PocketQuant/
├── configs/                    # Configuration files
│   └── config.yaml            # Main project configuration
├── data/                       # Data storage
│   ├── merchant_liquidity.csv # Raw dataset
│   ├── processed/             # Cleaned data
│   └── features/              # Engineered features
├── docs/                       # Documentation
│   ├── PROJECT_CHARTER.md     # Project charter
│   └── ARCHITECTURE.md        # System architecture
├── models/                     # Model artifacts
│   ├── trained/               # Serialized models
│   └── artifacts/             # Scalers, encoders
├── notebooks/                  # Jupyter notebooks
├── reports/                    # Evaluation reports
│   └── figures/               # Visualizations
├── src/                        # Source code
│   ├── data/                  # Data loading & processing
│   ├── features/              # Feature engineering
│   ├── models/                # Model training
│   ├── evaluation/            # Model evaluation
│   └── utils/                 # Utility functions
└── tests/                      # Unit tests
```

## 📊 Dataset

The dataset contains **50,000+ records** with **59 features** including:
- Merchant demographics
- Transaction metrics
- Cash flow indicators
- Settlement data
- Risk scores
- Credit utilization

**Target Variable:** `liquidity_shortage_next_48h` (0 = No shortage, 1 = Shortage expected)

## 📈 Evaluation Metrics

| Metric | Target |
|--------|--------|
| Precision | > 0.75 |
| Recall | > 0.80 |
| F1-Score | > 0.77 |
| ROC-AUC | > 0.85 |

## ⚠️ Risk Classification

| Risk Level | Probability | Action |
|------------|-------------|--------|
| Low | 0.00 - 0.30 | Standard monitoring |
| Medium | 0.30 - 0.60 | Enhanced monitoring |
| High | 0.60 - 0.80 | Immediate intervention |
| Critical | 0.80 - 1.00 | Urgent action |

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.9+
pip or conda
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/PocketQuant.git
cd PocketQuant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Usage

```python
# Load configuration
import yaml
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Run training pipeline (coming in Phase 2)
# python src/train.py
```

## 📁 Documentation

- [Project Charter](docs/PROJECT_CHARTER.md) - Business objectives, metrics, and scope
- [Architecture](docs/ARCHITECTURE.md) - System design and data flow

## 🛠️ Technology Stack

- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, XGBoost, LightGBM
- **Visualization:** Matplotlib, Seaborn
- **Configuration:** YAML

## 📅 Roadmap

- [x] Phase 1: Project Foundation & Technical Planning
- [ ] Phase 2: Exploratory Data Analysis
- [ ] Phase 3: Feature Engineering
- [ ] Phase 4: Model Development
- [ ] Phase 5: Evaluation & Optimization
- [ ] Phase 6: Documentation & Delivery

## 📄 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please read the contribution guidelines before submitting PRs.

---

*Built with ❤️ by the PocketQuant Team*
