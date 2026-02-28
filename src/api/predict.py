"""
Prediction service for PocketQuant Liquidity Risk Model.
Handles model loading, feature preparation, and prediction.
"""
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Model path
MODEL_DIR = Path(__file__).parent.parent.parent / "models" / "trained"
MODEL_PATH = MODEL_DIR / "xgboost_liquidity_model.pkl"

# Feature list for model input (must match training order)
FEATURE_COLUMNS = [
    'daily_inflow', 'daily_outflow_estimated', 'net_cash_flow', 'transaction_count',
    'inflow_outflow_ratio', 'rolling_3d_inflow', 'rolling_7d_inflow', 'rolling_14d_inflow',
    'rolling_7d_outflow', 'rolling_7d_net_cashflow', 'rolling_7d_inflow_cv',
    'rolling_7d_volatility', 'stress_score_composite', 'stress_intensity_score',
    'volatility_score_normalized', 'credit_utilization_ratio', 'liquidity_buffer_days',
    'liquidity_buffer_ratio', 'cashflow_coverage_ratio', 'working_capital_indicator',
    'debt_service_ratio', 'revenue_decline_pct', 'consecutive_drop_days',
    'credit_vol_interaction', 'stress_buffer_interaction', 'revdrop_credit_interaction',
    'gap_volatility_interaction', 'revenue_drop_7d', 'revenue_drop_significant',
    'revenue_drop_severe', 'month', 'is_weekend',
    'merchant_category_encoded', 'merchant_sub_category_encoded',
    'merchant_city_encoded', 'merchant_state_encoded',
    'kyc_status_encoded', 'risk_segment_internal_encoded',
    'merchant_category_Food', 'merchant_category_Grocery',
    'merchant_category_Pharmacy', 'merchant_category_Retail',
    'merchant_sub_category_Medical', 'merchant_sub_category_MobileShop',
    'merchant_sub_category_Restaurant', 'merchant_sub_category_Supermarket',
    'merchant_city_Delhi', 'merchant_city_Mumbai',
    'merchant_city_Pune', 'merchant_city_Surat',
    'merchant_state_Gujarat', 'merchant_state_Maharashtra',
    'kyc_status_Verified', 'risk_segment_internal_Low', 'risk_segment_internal_Medium'
]

# Feature importance for risk factor analysis
TOP_FEATURES = [
    ('liquidity_buffer_ratio', 'Low liquidity buffer ratio'),
    ('credit_utilization_ratio', 'High credit utilization'),
    ('rolling_7d_volatility', 'High cash flow volatility'),
    ('stress_score_composite', 'Elevated stress indicators'),
    ('revenue_decline_pct', 'Revenue decline detected'),
    ('liquidity_buffer_days', 'Insufficient buffer days'),
    ('debt_service_ratio', 'High debt service burden')
]

# Category encodings
CATEGORY_ENCODING = {
    'merchant_category': {'Food': 0, 'Grocery': 1, 'Pharmacy': 2, 'Retail': 3, 'Other': 4},
    'merchant_city': {'Delhi': 0, 'Mumbai': 1, 'Pune': 2, 'Surat': 3, 'Other': 4},
    'merchant_state': {'Gujarat': 0, 'Maharashtra': 1, 'Other': 2},
    'kyc_status': {'Verified': 0, 'Pending': 1, 'Rejected': 2},
    'risk_segment_internal': {'Low': 0, 'Medium': 1, 'High': 2}
}

SUB_CATEGORY_ENCODING = {
    'Medical': 0, 'MobileShop': 1, 'Restaurant': 2, 'Supermarket': 3, 'Other': 4
}


class LiquidityRiskPredictor:
    """
    Liquidity risk prediction service.
    Loads XGBoost model and provides prediction interface.
    """
    
    def __init__(self, model_path: str = None, threshold: float = 0.40):
        """
        Initialize predictor with model.
        
        Args:
            model_path: Path to trained model pickle file
            threshold: Decision threshold for risk classification
        """
        self.model_path = Path(model_path) if model_path else MODEL_PATH
        self.threshold = threshold
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def _prepare_features(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Transform input data to feature vector matching training format.
        
        Args:
            input_data: Dictionary of input features
            
        Returns:
            DataFrame with features in correct order
        """
        features = {}
        
        # Direct numeric features
        numeric_fields = [
            'daily_inflow', 'daily_outflow_estimated', 'net_cash_flow', 'transaction_count',
            'inflow_outflow_ratio', 'rolling_3d_inflow', 'rolling_7d_inflow', 'rolling_14d_inflow',
            'rolling_7d_outflow', 'rolling_7d_net_cashflow', 'rolling_7d_inflow_cv',
            'rolling_7d_volatility', 'stress_score_composite', 'stress_intensity_score',
            'volatility_score_normalized', 'credit_utilization_ratio', 'liquidity_buffer_days',
            'liquidity_buffer_ratio', 'cashflow_coverage_ratio', 'working_capital_indicator',
            'debt_service_ratio', 'revenue_decline_pct', 'consecutive_drop_days',
            'credit_vol_interaction', 'stress_buffer_interaction', 'revdrop_credit_interaction',
            'gap_volatility_interaction', 'revenue_drop_7d', 'revenue_drop_significant',
            'revenue_drop_severe', 'month', 'is_weekend'
        ]
        
        for field in numeric_fields:
            features[field] = input_data.get(field, 0)
        
        # Encode categorical features
        merchant_cat = input_data.get('merchant_category', 'Other')
        merchant_city = input_data.get('merchant_city', 'Other')
        merchant_state = input_data.get('merchant_state', 'Other')
        kyc_status = input_data.get('kyc_status', 'Verified')
        risk_segment = input_data.get('risk_segment_internal', 'Medium')
        sub_category = input_data.get('merchant_sub_category', 'Other')
        
        # Label encoded features
        features['merchant_category_encoded'] = CATEGORY_ENCODING['merchant_category'].get(merchant_cat, 4)
        features['merchant_sub_category_encoded'] = SUB_CATEGORY_ENCODING.get(sub_category, 4)
        features['merchant_city_encoded'] = CATEGORY_ENCODING['merchant_city'].get(merchant_city, 4)
        features['merchant_state_encoded'] = CATEGORY_ENCODING['merchant_state'].get(merchant_state, 2)
        features['kyc_status_encoded'] = CATEGORY_ENCODING['kyc_status'].get(kyc_status, 1)
        features['risk_segment_internal_encoded'] = CATEGORY_ENCODING['risk_segment_internal'].get(risk_segment, 1)
        
        # One-hot encoded features
        features['merchant_category_Food'] = 1 if merchant_cat == 'Food' else 0
        features['merchant_category_Grocery'] = 1 if merchant_cat == 'Grocery' else 0
        features['merchant_category_Pharmacy'] = 1 if merchant_cat == 'Pharmacy' else 0
        features['merchant_category_Retail'] = 1 if merchant_cat == 'Retail' else 0
        
        features['merchant_sub_category_Medical'] = 1 if sub_category == 'Medical' else 0
        features['merchant_sub_category_MobileShop'] = 1 if sub_category == 'MobileShop' else 0
        features['merchant_sub_category_Restaurant'] = 1 if sub_category == 'Restaurant' else 0
        features['merchant_sub_category_Supermarket'] = 1 if sub_category == 'Supermarket' else 0
        
        features['merchant_city_Delhi'] = 1 if merchant_city == 'Delhi' else 0
        features['merchant_city_Mumbai'] = 1 if merchant_city == 'Mumbai' else 0
        features['merchant_city_Pune'] = 1 if merchant_city == 'Pune' else 0
        features['merchant_city_Surat'] = 1 if merchant_city == 'Surat' else 0
        
        features['merchant_state_Gujarat'] = 1 if merchant_state == 'Gujarat' else 0
        features['merchant_state_Maharashtra'] = 1 if merchant_state == 'Maharashtra' else 0
        
        features['kyc_status_Verified'] = 1 if kyc_status == 'Verified' else 0
        features['risk_segment_internal_Low'] = 1 if risk_segment == 'Low' else 0
        features['risk_segment_internal_Medium'] = 1 if risk_segment == 'Medium' else 0
        
        # Create DataFrame with correct column order
        df = pd.DataFrame([features])
        df = df[FEATURE_COLUMNS]
        
        return df
    
    def _identify_risk_factors(self, input_data: Dict[str, Any]) -> List[str]:
        """
        Identify top risk factors based on input values.
        
        Args:
            input_data: Input features dictionary
            
        Returns:
            List of risk factor descriptions
        """
        risk_factors = []
        
        # Check key risk indicators
        if input_data.get('liquidity_buffer_ratio', 999) < 3:
            risk_factors.append("Low liquidity buffer ratio (< 3)")
        
        if input_data.get('credit_utilization_ratio', 0) > 0.7:
            risk_factors.append("High credit utilization (> 70%)")
        
        if input_data.get('rolling_7d_volatility', 0) > 0.3:
            risk_factors.append("High cash flow volatility")
        
        if input_data.get('stress_score_composite', 0) > 0.5:
            risk_factors.append("Elevated stress indicators")
        
        if input_data.get('revenue_decline_pct', 0) < -0.1:
            risk_factors.append("Significant revenue decline")
        
        if input_data.get('liquidity_buffer_days', 999) < 3:
            risk_factors.append("Insufficient buffer days (< 3)")
        
        if input_data.get('debt_service_ratio', 0) > 0.4:
            risk_factors.append("High debt service burden")
        
        if input_data.get('consecutive_drop_days', 0) >= 3:
            risk_factors.append("Consecutive revenue drop days")
        
        return risk_factors[:5]  # Return top 5
    
    def _get_recommendation(self, risk_probability: float) -> str:
        """
        Generate action recommendation based on risk level.
        
        Args:
            risk_probability: Predicted probability of shortage
            
        Returns:
            Recommendation string
        """
        if risk_probability >= 0.8:
            return "CRITICAL: Immediate intervention required. Initiate proactive outreach and credit review."
        elif risk_probability >= 0.6:
            return "HIGH RISK: Recommend review within 24 hours. Consider credit line adjustment."
        elif risk_probability >= 0.4:
            return "MODERATE RISK: Monitor closely. Schedule periodic review."
        elif risk_probability >= 0.2:
            return "LOW RISK: Standard monitoring. No immediate action required."
        else:
            return "MINIMAL RISK: Merchant shows healthy liquidity. Continue routine monitoring."
    
    def _get_confidence(self, risk_probability: float) -> str:
        """
        Determine prediction confidence based on probability extremity.
        
        Args:
            risk_probability: Predicted probability
            
        Returns:
            Confidence level string
        """
        if risk_probability < 0.15 or risk_probability > 0.85:
            return "High"
        elif risk_probability < 0.30 or risk_probability > 0.70:
            return "Medium"
        else:
            return "Low"
    
    def predict(self, input_data: Dict[str, Any], merchant_id: str = None) -> Dict[str, Any]:
        """
        Make risk prediction for a merchant.
        
        Args:
            input_data: Dictionary of merchant features
            merchant_id: Optional merchant identifier
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")
        
        # Prepare features
        X = self._prepare_features(input_data)
        
        # Get prediction
        probability = float(self.model.predict_proba(X)[0, 1])  # Convert to Python float
        risk_label = "High Risk" if probability >= self.threshold else "Low Risk"
        risk_score = int(probability * 100)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(input_data)
        
        # Generate recommendation
        recommendation = self._get_recommendation(probability)
        
        # Determine confidence
        confidence = self._get_confidence(probability)
        
        return {
            "merchant_id": merchant_id,
            "risk_probability": round(probability, 4),
            "risk_label": risk_label,
            "risk_score": risk_score,
            "threshold_used": self.threshold,
            "confidence": confidence,
            "top_risk_factors": risk_factors,
            "recommendation": recommendation
        }


# Global predictor instance (loaded once at startup)
_predictor = None


def get_predictor(threshold: float = 0.40) -> LiquidityRiskPredictor:
    """
    Get or create global predictor instance.
    
    Args:
        threshold: Decision threshold
        
    Returns:
        LiquidityRiskPredictor instance
    """
    global _predictor
    if _predictor is None:
        _predictor = LiquidityRiskPredictor(threshold=threshold)
    return _predictor
