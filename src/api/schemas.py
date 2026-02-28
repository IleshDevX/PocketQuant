"""
Pydantic schemas for request/response validation.
PocketQuant Liquidity Risk Prediction API
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


class MerchantCategory(str, Enum):
    """Valid merchant categories."""
    FOOD = "Food"
    GROCERY = "Grocery"
    PHARMACY = "Pharmacy"
    RETAIL = "Retail"
    OTHER = "Other"


class MerchantCity(str, Enum):
    """Major merchant cities."""
    DELHI = "Delhi"
    MUMBAI = "Mumbai"
    PUNE = "Pune"
    SURAT = "Surat"
    OTHER = "Other"


class MerchantState(str, Enum):
    """Merchant states."""
    GUJARAT = "Gujarat"
    MAHARASHTRA = "Maharashtra"
    OTHER = "Other"


class KYCStatus(str, Enum):
    """KYC verification status."""
    VERIFIED = "Verified"
    PENDING = "Pending"
    REJECTED = "Rejected"


class RiskSegment(str, Enum):
    """Internal risk segment classification."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class MerchantInput(BaseModel):
    """
    Input schema for merchant liquidity risk prediction.
    Contains financial metrics and merchant profile data.
    """
    # Core financial metrics
    daily_inflow: float = Field(..., ge=0, description="Daily cash inflow amount")
    daily_outflow_estimated: float = Field(..., ge=0, description="Estimated daily outflow")
    net_cash_flow: float = Field(..., description="Net cash flow (inflow - outflow)")
    transaction_count: int = Field(..., ge=0, description="Number of transactions")
    
    # Ratios and indicators
    inflow_outflow_ratio: float = Field(..., ge=0, description="Ratio of inflow to outflow")
    credit_utilization_ratio: float = Field(..., ge=0, le=2, description="Credit utilization (0-2)")
    liquidity_buffer_days: float = Field(..., ge=0, description="Days of liquidity buffer")
    liquidity_buffer_ratio: float = Field(..., ge=0, description="Liquidity buffer ratio")
    cashflow_coverage_ratio: float = Field(..., description="Cash flow coverage ratio")
    working_capital_indicator: float = Field(..., description="Working capital indicator")
    debt_service_ratio: float = Field(..., ge=0, description="Debt service ratio")
    
    # Rolling metrics
    rolling_3d_inflow: float = Field(..., ge=0, description="3-day rolling inflow")
    rolling_7d_inflow: float = Field(..., ge=0, description="7-day rolling inflow")
    rolling_14d_inflow: float = Field(..., ge=0, description="14-day rolling inflow")
    rolling_7d_outflow: float = Field(..., ge=0, description="7-day rolling outflow")
    rolling_7d_net_cashflow: float = Field(..., description="7-day rolling net cash flow")
    rolling_7d_inflow_cv: float = Field(..., ge=0, description="7-day inflow coefficient of variation")
    rolling_7d_volatility: float = Field(..., ge=0, description="7-day cash flow volatility")
    
    # Stress and risk scores
    stress_score_composite: float = Field(..., ge=0, description="Composite stress score")
    stress_intensity_score: float = Field(..., ge=0, description="Stress intensity score")
    volatility_score_normalized: float = Field(..., ge=0, le=1, description="Normalized volatility score")
    
    # Revenue metrics
    revenue_decline_pct: float = Field(..., ge=-1, le=1, description="Revenue decline percentage")
    consecutive_drop_days: int = Field(..., ge=0, description="Consecutive days of revenue drop")
    revenue_drop_7d: float = Field(default=0, description="7-day revenue drop indicator")
    revenue_drop_significant: int = Field(default=0, ge=0, le=1, description="Significant revenue drop flag")
    revenue_drop_severe: int = Field(default=0, ge=0, le=1, description="Severe revenue drop flag")
    
    # Interaction features
    credit_vol_interaction: float = Field(default=0, description="Credit-volatility interaction")
    stress_buffer_interaction: float = Field(default=0, description="Stress-buffer interaction")
    revdrop_credit_interaction: float = Field(default=0, description="Revenue drop-credit interaction")
    gap_volatility_interaction: float = Field(default=0, description="Gap-volatility interaction")
    
    # Temporal features
    month: int = Field(..., ge=1, le=12, description="Month of the year")
    is_weekend: int = Field(..., ge=0, le=1, description="Weekend indicator")
    
    # Merchant profile
    merchant_category: MerchantCategory = Field(..., description="Merchant business category")
    merchant_sub_category: Optional[str] = Field(default=None, description="Sub-category")
    merchant_city: MerchantCity = Field(..., description="Merchant city")
    merchant_state: MerchantState = Field(..., description="Merchant state")
    kyc_status: KYCStatus = Field(default=KYCStatus.VERIFIED, description="KYC status")
    risk_segment_internal: RiskSegment = Field(default=RiskSegment.MEDIUM, description="Internal risk segment")
    
    @field_validator('liquidity_buffer_ratio')
    @classmethod
    def validate_buffer_ratio(cls, v):
        if v < 0:
            raise ValueError('liquidity_buffer_ratio must be non-negative')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "daily_inflow": 15000.0,
                "daily_outflow_estimated": 12000.0,
                "net_cash_flow": 3000.0,
                "transaction_count": 45,
                "inflow_outflow_ratio": 1.25,
                "credit_utilization_ratio": 0.4,
                "liquidity_buffer_days": 5.5,
                "liquidity_buffer_ratio": 4.2,
                "cashflow_coverage_ratio": 1.8,
                "working_capital_indicator": 0.3,
                "debt_service_ratio": 0.25,
                "rolling_3d_inflow": 14500.0,
                "rolling_7d_inflow": 14200.0,
                "rolling_14d_inflow": 13800.0,
                "rolling_7d_outflow": 11500.0,
                "rolling_7d_net_cashflow": 2700.0,
                "rolling_7d_inflow_cv": 0.15,
                "rolling_7d_volatility": 0.12,
                "stress_score_composite": 0.25,
                "stress_intensity_score": 0.18,
                "volatility_score_normalized": 0.22,
                "revenue_decline_pct": -0.05,
                "consecutive_drop_days": 1,
                "revenue_drop_7d": 0.0,
                "revenue_drop_significant": 0,
                "revenue_drop_severe": 0,
                "credit_vol_interaction": 0.05,
                "stress_buffer_interaction": 1.05,
                "revdrop_credit_interaction": -0.02,
                "gap_volatility_interaction": 0.03,
                "month": 2,
                "is_weekend": 0,
                "merchant_category": "Retail",
                "merchant_sub_category": "MobileShop",
                "merchant_city": "Mumbai",
                "merchant_state": "Maharashtra",
                "kyc_status": "Verified",
                "risk_segment_internal": "Low"
            }
        }


class RiskPrediction(BaseModel):
    """
    Output schema for risk prediction response.
    """
    merchant_id: Optional[str] = Field(default=None, description="Merchant identifier if provided")
    risk_probability: float = Field(..., ge=0, le=1, description="Probability of liquidity shortage")
    risk_label: str = Field(..., description="Risk classification (High Risk / Low Risk)")
    risk_score: int = Field(..., ge=0, le=100, description="Risk score (0-100)")
    threshold_used: float = Field(..., description="Decision threshold used")
    confidence: str = Field(..., description="Prediction confidence level")
    
    # Top risk factors
    top_risk_factors: List[str] = Field(default=[], description="Top contributing risk factors")
    
    # Recommendations
    recommendation: str = Field(..., description="Action recommendation based on risk level")

    class Config:
        json_schema_extra = {
            "example": {
                "merchant_id": "M12345",
                "risk_probability": 0.72,
                "risk_label": "High Risk",
                "risk_score": 72,
                "threshold_used": 0.40,
                "confidence": "High",
                "top_risk_factors": [
                    "Low liquidity buffer ratio",
                    "High credit utilization",
                    "Revenue decline detected"
                ],
                "recommendation": "Immediate review recommended. Consider proactive outreach."
            }
        }


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    model_loaded: bool
    version: str
    timestamp: str


class BatchPredictionRequest(BaseModel):
    """Batch prediction request for multiple merchants."""
    merchants: List[MerchantInput] = Field(..., min_length=1, max_length=100)


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    predictions: List[RiskPrediction]
    total_processed: int
    high_risk_count: int
    processing_time_ms: float
