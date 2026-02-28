"""
Logging configuration for PocketQuant API.
Logs predictions for audit trail and monitoring.
"""
import logging
import json
from datetime import datetime
from pathlib import Path
import os

# Create logs directory
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure main logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("pocketquant_api")

# Prediction logger (separate file for audit)
prediction_logger = logging.getLogger("predictions")
prediction_handler = logging.FileHandler(LOG_DIR / "predictions.log")
prediction_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
prediction_logger.addHandler(prediction_handler)
prediction_logger.setLevel(logging.INFO)


def log_prediction(
    request_id: str,
    input_data: dict,
    prediction: dict,
    processing_time_ms: float
):
    """
    Log prediction for audit trail.
    
    Args:
        request_id: Unique request identifier
        input_data: Input features (sanitized)
        prediction: Model prediction output
        processing_time_ms: Time taken for prediction
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "input_summary": {
            "liquidity_buffer_ratio": input_data.get("liquidity_buffer_ratio"),
            "credit_utilization_ratio": input_data.get("credit_utilization_ratio"),
            "merchant_category": input_data.get("merchant_category"),
            "daily_inflow": input_data.get("daily_inflow")
        },
        "prediction": {
            "risk_probability": prediction.get("risk_probability"),
            "risk_label": prediction.get("risk_label"),
            "risk_score": prediction.get("risk_score")
        },
        "processing_time_ms": processing_time_ms
    }
    
    prediction_logger.info(json.dumps(log_entry))
    return log_entry


def log_error(error_type: str, error_message: str, request_id: str = None):
    """Log API errors."""
    logger.error(f"[{request_id}] {error_type}: {error_message}")


def log_startup(model_path: str, model_loaded: bool):
    """Log API startup."""
    logger.info(f"API Starting - Model Path: {model_path}, Loaded: {model_loaded}")


def log_request(endpoint: str, method: str, request_id: str):
    """Log incoming request."""
    logger.info(f"[{request_id}] {method} {endpoint}")
