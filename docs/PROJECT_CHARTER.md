# PocketQuant: Merchant Liquidity Shortage Prediction

## Project Charter

**Version:** 1.0  
**Date:** February 26, 2026  
**Project Owner:** PocketQuant Team

---

## 1. Business Objective

**Primary Goal:** Predict `liquidity_shortage_next_48h` for merchants to enable proactive risk management and intervention.

**Business Value:**
- Early identification of merchants at risk of liquidity shortages
- Enable proactive support and credit line adjustments
- Reduce default rates and merchant churn
- Optimize working capital allocation

---

## 2. Problem Statement

Merchants operating on payment platforms face liquidity challenges due to:
- Irregular cash flows
- Settlement delays
- Unexpected expense spikes
- Seasonal variations

Early prediction of liquidity shortages allows the platform to:
- Offer timely credit facilities
- Adjust settlement schedules
- Provide financial guidance
- Mitigate platform risk exposure
 
---

## 3. Modeling Approach

### 3.1 Task Type
**Binary Classification**

- **Target Variable:** `liquidity_shortage_next_48h`
  - `0` = No shortage expected
  - `1` = Shortage expected

### 3.2 Input Assumption
Model uses **historical engineered features** including:
- Merchant demographics (category, location, business age)
- Transaction metrics (daily inflow, count, ticket sizes)
- Cash flow indicators (inflow/outflow ratios, net cash flow)
- Settlement data (delays, success rates, pending amounts)
- Financial health metrics (balances, liquidity buffer days)
- Rolling statistics (3-day, 7-day averages, volatility)
- Risk indicators (stress scores, expense spikes, concentration)
- Credit utilization (limits, outstanding loans, defaults)
- Temporal features (weekend, festival, day of week, month)

### 3.3 Feature Categories

| Category | Features | Description |
|----------|----------|-------------|
| Merchant Info | merchant_category, merchant_city, business_age_days, kyc_status, risk_segment_internal | Static merchant attributes |
| Transaction | daily_inflow, transaction_count, avg_ticket_size, failed_transaction_count | Daily transaction metrics |
| Cash Flow | daily_outflow_estimated, net_cash_flow, inflow_outflow_ratio | Cash movement indicators |
| Settlement | settlement_delay_days, pending_settlement_amount, settlement_success_rate | Settlement health |
| Balance | wallet_balance, bank_balance_visible, opening_balance, closing_balance | Account balances |
| Rolling Stats | rolling_3d_inflow_avg, rolling_7d_inflow_avg, rolling_7d_volatility | Temporal aggregations |
| Risk Indicators | stress_score_composite, volatility_score_normalized, expense_spike_flag | Risk metrics |
| Credit | credit_limit_assigned, credit_utilization_ratio, outstanding_loan_amount | Credit health |
| Temporal | is_weekend, is_festival, weekday_number, month | Time-based features |

---

## 4. Evaluation Metrics

### 4.1 Primary Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Precision** | Accuracy of positive predictions | > 0.75 |
| **Recall** | Coverage of actual positives | > 0.80 |
| **F1-Score** | Harmonic mean of precision/recall | > 0.77 |
| **ROC-AUC** | Overall discriminative ability | > 0.85 |

### 4.2 Metric Prioritization
Given the business context:
1. **Recall** is prioritized to minimize missed shortages (false negatives)
2. **Precision** ensures interventions are cost-effective
3. **F1-Score** provides balanced assessment
4. **ROC-AUC** validates model's ranking ability

---

## 5. Risk Classification Thresholds

### 5.1 Probability Thresholds

| Risk Level | Probability Range | Action |
|------------|-------------------|--------|
| **Low Risk** | 0.00 - 0.30 | Standard monitoring |
| **Medium Risk** | 0.30 - 0.60 | Enhanced monitoring, proactive outreach |
| **High Risk** | 0.60 - 0.80 | Immediate intervention, credit review |
| **Critical Risk** | 0.80 - 1.00 | Urgent action, settlement hold review |

### 5.2 Decision Matrix

| Predicted | Actual | Outcome | Business Impact |
|-----------|--------|---------|-----------------|
| High | Shortage | True Positive (TP) | Successful intervention |
| High | No Shortage | False Positive (FP) | Unnecessary intervention cost |
| Low | No Shortage | True Negative (TN) | Correct non-intervention |
| Low | Shortage | False Negative (FN) | Missed intervention (high cost) |

### 5.3 Threshold Optimization Strategy
- Default threshold: **0.50**
- Operational threshold: **0.40** (favoring recall)
- Threshold will be optimized based on:
  - Cost of intervention vs. cost of missed shortage
  - Precision-Recall tradeoff analysis
  - Business capacity for interventions

---

## 6. Project Scope

### 6.1 In Scope
- Binary classification model development
- Feature engineering pipeline
- Model training and evaluation
- Threshold optimization
- Model documentation
- Basic API structure for predictions

### 6.2 Out of Scope (Phase 1)
- Real-time streaming predictions
- Model deployment to production
- A/B testing framework
- Continuous learning pipeline
- Multi-class severity prediction

---

## 7. Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Model Performance | ROC-AUC > 0.85 | Cross-validation score |
| Recall Achievement | > 80% | Test set evaluation |
| False Positive Rate | < 30% | Test set evaluation |
| Documentation | Complete | All deliverables produced |

---

## 8. Assumptions

1. Historical data is representative of future patterns
2. Feature engineering captures relevant signals
3. 48-hour prediction horizon is actionable
4. Data quality is sufficient for modeling
5. No significant concept drift in short term

---

## 9. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Class imbalance | Model bias toward majority | High | SMOTE, class weights, threshold tuning |
| Feature leakage | Overfitting | Medium | Careful temporal validation |
| Data quality issues | Poor predictions | Medium | EDA, outlier handling |
| Concept drift | Model degradation | Medium | Monitoring, periodic retraining |

---

## 10. Timeline (Phase 1)

| Milestone | Duration | Status |
|-----------|----------|--------|
| Project Setup | Day 1 | ✅ Complete |
| EDA & Data Understanding | Days 2-3 | Pending |
| Feature Engineering | Days 4-5 | Pending |
| Model Development | Days 6-8 | Pending |
| Evaluation & Tuning | Days 9-10 | Pending |
| Documentation & Delivery | Day 11 | Pending |

---

## 11. Stakeholders

| Role | Responsibility |
|------|----------------|
| Data Science Team | Model development, evaluation |
| Risk Management | Threshold definition, business rules |
| Product Team | Integration requirements |
| Operations | Intervention capacity planning |

---

## 12. Deliverables

### Phase 1 Deliverables
- [x] Project Charter Document
- [x] Final Architecture Diagram
- [x] Folder Structure
- [ ] GitHub Repository Initialized
- [ ] EDA Notebook
- [ ] Feature Engineering Pipeline
- [ ] Trained Model
- [ ] Evaluation Report

---

*Document maintained by PocketQuant Data Science Team*
