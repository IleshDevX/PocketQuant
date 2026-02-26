# PocketQuant - ML Pipeline Architecture

## System Architecture Diagram

```mermaid
flowchart TB
    subgraph DATA["📊 Data Layer"]
        RAW[(Raw Data<br/>merchant_liquidity.csv)]
        PROCESSED[(Processed Data)]
        FEATURES[(Feature Store)]
    end

    subgraph PIPELINE["⚙️ ML Pipeline"]
        direction TB
        
        subgraph INGESTION["Data Ingestion"]
            LOAD[Load Data]
            VALIDATE[Data Validation]
            CLEAN[Data Cleaning]
        end
        
        subgraph FEATURE_ENG["Feature Engineering"]
            TRANSFORM[Feature Transformation]
            ENCODE[Categorical Encoding]
            SCALE[Feature Scaling]
            SELECT[Feature Selection]
        end
        
        subgraph TRAINING["Model Training"]
            SPLIT[Train/Test Split]
            BALANCE[Class Balancing]
            TRAIN[Model Training]
            TUNE[Hyperparameter Tuning]
        end
        
        subgraph EVALUATION["Model Evaluation"]
            METRICS[Calculate Metrics<br/>Precision, Recall, F1, AUC]
            THRESHOLD[Threshold Optimization]
            VALIDATE_MODEL[Cross-Validation]
        end
    end

    subgraph OUTPUT["📤 Output Layer"]
        MODEL[(Trained Model)]
        ARTIFACTS[(Model Artifacts<br/>Scalers, Encoders)]
        REPORTS[Evaluation Reports]
    end

    subgraph INFERENCE["🔮 Inference"]
        PREDICT[Prediction Service]
        RISK[Risk Classification<br/>Low/Medium/High/Critical]
    end

    %% Data Flow
    RAW --> LOAD
    LOAD --> VALIDATE
    VALIDATE --> CLEAN
    CLEAN --> PROCESSED
    
    PROCESSED --> TRANSFORM
    TRANSFORM --> ENCODE
    ENCODE --> SCALE
    SCALE --> SELECT
    SELECT --> FEATURES
    
    FEATURES --> SPLIT
    SPLIT --> BALANCE
    BALANCE --> TRAIN
    TRAIN --> TUNE
    
    TUNE --> METRICS
    METRICS --> THRESHOLD
    THRESHOLD --> VALIDATE_MODEL
    
    VALIDATE_MODEL --> MODEL
    VALIDATE_MODEL --> ARTIFACTS
    VALIDATE_MODEL --> REPORTS
    
    MODEL --> PREDICT
    ARTIFACTS --> PREDICT
    PREDICT --> RISK

    %% Styling
    classDef dataNode fill:#e1f5fe,stroke:#01579b
    classDef processNode fill:#f3e5f5,stroke:#4a148c
    classDef outputNode fill:#e8f5e9,stroke:#1b5e20
    classDef inferenceNode fill:#fff3e0,stroke:#e65100
    
    class RAW,PROCESSED,FEATURES dataNode
    class LOAD,VALIDATE,CLEAN,TRANSFORM,ENCODE,SCALE,SELECT,SPLIT,BALANCE,TRAIN,TUNE,METRICS,THRESHOLD,VALIDATE_MODEL processNode
    class MODEL,ARTIFACTS,REPORTS outputNode
    class PREDICT,RISK inferenceNode
```

## Component Details

### 1. Data Layer
| Component | Description | Location |
|-----------|-------------|----------|
| Raw Data | Original merchant liquidity dataset | `data/merchant_liquidity.csv` |
| Processed Data | Cleaned and validated data | `data/processed/` |
| Feature Store | Engineered features ready for modeling | `data/features/` |

### 2. ML Pipeline Components

#### Data Ingestion
- **Load Data**: Read CSV with proper dtypes
- **Data Validation**: Schema validation, null checks
- **Data Cleaning**: Handle missing values, outliers

#### Feature Engineering
- **Feature Transformation**: Log transforms, ratios
- **Categorical Encoding**: Label/One-hot encoding
- **Feature Scaling**: StandardScaler/MinMaxScaler
- **Feature Selection**: Correlation, importance-based

#### Model Training
- **Train/Test Split**: Temporal split with 80/20 ratio
- **Class Balancing**: SMOTE, class weights
- **Model Training**: Multiple algorithm comparison
- **Hyperparameter Tuning**: GridSearchCV, Optuna

#### Model Evaluation
- **Metrics**: Precision, Recall, F1, ROC-AUC
- **Threshold Optimization**: PR curve analysis
- **Cross-Validation**: Stratified K-Fold

### 3. Output Layer
| Component | Format | Location |
|-----------|--------|----------|
| Trained Model | `.joblib` | `models/trained/` |
| Artifacts | `.pkl` | `models/artifacts/` |
| Reports | `.html`, `.json` | `reports/` |

### 4. Inference Layer
- **Prediction Service**: Batch/single prediction capability
- **Risk Classification**: Probability to risk level mapping

## Data Flow Summary

```
Raw Data → Ingestion → Processing → Feature Engineering → Training → Evaluation → Model Export
                                                                              ↓
                                                                    Inference Pipeline
```

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Data Processing | Pandas, NumPy |
| Feature Engineering | Scikit-learn, Feature-engine |
| Modeling | Scikit-learn, XGBoost, LightGBM |
| Evaluation | Scikit-learn metrics, Matplotlib |
| Experiment Tracking | MLflow (optional) |
| Serialization | Joblib, Pickle |

---

*Architecture document for PocketQuant Liquidity Prediction System*
