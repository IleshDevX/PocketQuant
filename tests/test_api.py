"""
Test script for PocketQuant Liquidity Risk API.
Run this after starting the API server.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Sample test payload
sample_merchant = {
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

# High risk merchant (low liquidity buffer)
high_risk_merchant = {
    "daily_inflow": 5000.0,
    "daily_outflow_estimated": 8000.0,
    "net_cash_flow": -3000.0,
    "transaction_count": 15,
    "inflow_outflow_ratio": 0.625,
    "credit_utilization_ratio": 0.85,
    "liquidity_buffer_days": 1.2,
    "liquidity_buffer_ratio": 1.5,
    "cashflow_coverage_ratio": 0.6,
    "working_capital_indicator": -0.2,
    "debt_service_ratio": 0.55,
    "rolling_3d_inflow": 4800.0,
    "rolling_7d_inflow": 5200.0,
    "rolling_14d_inflow": 6000.0,
    "rolling_7d_outflow": 8200.0,
    "rolling_7d_net_cashflow": -3000.0,
    "rolling_7d_inflow_cv": 0.45,
    "rolling_7d_volatility": 0.55,
    "stress_score_composite": 0.75,
    "stress_intensity_score": 0.68,
    "volatility_score_normalized": 0.72,
    "revenue_decline_pct": -0.25,
    "consecutive_drop_days": 5,
    "revenue_drop_7d": 1.0,
    "revenue_drop_significant": 1,
    "revenue_drop_severe": 1,
    "credit_vol_interaction": 0.47,
    "stress_buffer_interaction": 1.13,
    "revdrop_credit_interaction": -0.21,
    "gap_volatility_interaction": 0.15,
    "month": 2,
    "is_weekend": 0,
    "merchant_category": "Food",
    "merchant_sub_category": "Restaurant",
    "merchant_city": "Delhi",
    "merchant_state": "Maharashtra",
    "kyc_status": "Verified",
    "risk_segment_internal": "High"
}


def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 60)
    print("TEST: Health Check")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_predict_low_risk():
    """Test prediction for low-risk merchant."""
    print("\n" + "=" * 60)
    print("TEST: Predict Risk (Low Risk Merchant)")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/predict-risk",
        json=sample_merchant,
        params={"merchant_id": "TEST_LOW_001"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Risk Label: {data['risk_label']}")
        print(f"✅ Risk Score: {data['risk_score']}")
        print(f"✅ Probability: {data['risk_probability']}")
    
    return response.status_code == 200


def test_predict_high_risk():
    """Test prediction for high-risk merchant."""
    print("\n" + "=" * 60)
    print("TEST: Predict Risk (High Risk Merchant)")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/predict-risk",
        json=high_risk_merchant,
        params={"merchant_id": "TEST_HIGH_001"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Risk Label: {data['risk_label']}")
        print(f"✅ Risk Score: {data['risk_score']}")
        print(f"✅ Risk Factors: {data['top_risk_factors']}")
        print(f"✅ Recommendation: {data['recommendation']}")
    
    return response.status_code == 200


def test_batch_prediction():
    """Test batch prediction."""
    print("\n" + "=" * 60)
    print("TEST: Batch Prediction")
    print("=" * 60)
    
    batch_data = {
        "merchants": [sample_merchant, high_risk_merchant, sample_merchant]
    }
    
    response = requests.post(
        f"{BASE_URL}/predict-risk/batch",
        json=batch_data
    )
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Processed: {data['total_processed']}")
        print(f"High Risk Count: {data['high_risk_count']}")
        print(f"Processing Time: {data['processing_time_ms']:.2f} ms")
    
    return response.status_code == 200


def test_model_info():
    """Test model info endpoint."""
    print("\n" + "=" * 60)
    print("TEST: Model Info")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_validation_error():
    """Test input validation."""
    print("\n" + "=" * 60)
    print("TEST: Input Validation (Invalid Data)")
    print("=" * 60)
    
    invalid_data = {"daily_inflow": "not_a_number"}  # Invalid input
    
    response = requests.post(
        f"{BASE_URL}/predict-risk",
        json=invalid_data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Expected 422 (Validation Error): {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")
    return response.status_code == 422


def run_all_tests():
    """Run all API tests."""
    print("\n" + "=" * 60)
    print("POCKETQUANT API TEST SUITE")
    print("=" * 60)
    
    results = {
        "Health Check": test_health(),
        "Low Risk Prediction": test_predict_low_risk(),
        "High Risk Prediction": test_predict_high_risk(),
        "Batch Prediction": test_batch_prediction(),
        "Model Info": test_model_info(),
        "Validation Error": test_validation_error()
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server.")
        print("   Make sure the server is running with:")
        print("   uvicorn src.api.main:app --reload")
