"""
PocketQuant Liquidity Risk Prediction API
FastAPI backend service for merchant liquidity shortage prediction.

Version: 1.0.0
Author: PocketQuant Team
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uuid
import time
from datetime import datetime

from .schemas import (
    MerchantInput, RiskPrediction, HealthResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from .predict import get_predictor, LiquidityRiskPredictor
from .logger import log_prediction, log_error, log_startup, log_request, logger

# API Version
VERSION = "1.0.0"

# Global predictor
predictor: LiquidityRiskPredictor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - loads model at startup."""
    global predictor
    try:
        predictor = get_predictor(threshold=0.40)
        log_startup(str(predictor.model_path), predictor.is_loaded())
        logger.info(f"✅ PocketQuant API v{VERSION} started successfully")
        yield
    except Exception as e:
        log_error("STARTUP_ERROR", str(e))
        logger.error(f"❌ Failed to start API: {e}")
        raise
    finally:
        logger.info("API shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="PocketQuant Liquidity Risk API",
    description="""
    ## Merchant Liquidity Shortage Prediction Service
    
    This API predicts the probability of merchant liquidity shortages within the next 48 hours
    using a trained XGBoost machine learning model.
    
    ### Features:
    - **Single prediction**: Predict risk for one merchant
    - **Batch prediction**: Predict risk for multiple merchants
    - **Risk factors**: Identifies top contributing risk factors
    - **Recommendations**: Provides action recommendations
    
    ### Model Performance:
    - ROC-AUC: 0.999
    - Recall: 92.3%
    - Precision: 77.8%
    
    ### Decision Threshold:
    Default threshold is 0.40 (optimized for recall in risk management context).
    """,
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    request_id = getattr(request.state, 'request_id', 'unknown')
    log_error("HTTP_ERROR", f"{exc.status_code}: {exc.detail}", request_id)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "request_id": request_id}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    request_id = getattr(request.state, 'request_id', 'unknown')
    log_error("INTERNAL_ERROR", str(exc), request_id)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "request_id": request_id}
    )


# Middleware for request tracking
@app.middleware("http")
async def add_request_tracking(request: Request, call_next):
    """Add request ID and timing to all requests."""
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    
    start_time = time.time()
    log_request(request.url.path, request.method, request_id)
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"
    
    return response


# ==================== ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "service": "PocketQuant Liquidity Risk API",
        "version": VERSION,
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns API status and model availability.
    """
    return HealthResponse(
        status="healthy" if predictor and predictor.is_loaded() else "unhealthy",
        model_loaded=predictor.is_loaded() if predictor else False,
        version=VERSION,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/predict-risk", response_model=RiskPrediction, tags=["Predictions"])
async def predict_risk(
    request: Request,
    merchant: MerchantInput,
    merchant_id: str = None
):
    """
    Predict liquidity shortage risk for a single merchant.
    
    **Input**: Merchant financial metrics and profile data  
    **Output**: Risk probability, classification, and recommendations
    
    ### Risk Levels:
    - **High Risk** (probability >= 0.40): Requires attention
    - **Low Risk** (probability < 0.40): Normal monitoring
    
    ### Top Risk Factors:
    The response includes the top contributing factors to the risk score,
    helping identify what's driving the prediction.
    """
    if not predictor or not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Model not available")
    
    request_id = request.state.request_id
    start_time = time.time()
    
    try:
        # Convert Pydantic model to dict
        input_data = merchant.model_dump()
        
        # Make prediction
        prediction = predictor.predict(input_data, merchant_id=merchant_id)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Log prediction
        log_prediction(request_id, input_data, prediction, processing_time_ms)
        
        return RiskPrediction(**prediction)
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        log_error("PREDICTION_ERROR", str(e), request_id)
        raise HTTPException(status_code=500, detail="Prediction failed")


@app.post("/predict-risk/batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_risk_batch(
    request: Request,
    batch_request: BatchPredictionRequest
):
    """
    Predict liquidity shortage risk for multiple merchants (batch).
    
    **Max batch size**: 100 merchants  
    **Input**: Array of merchant data  
    **Output**: Array of predictions with summary statistics
    """
    if not predictor or not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Model not available")
    
    request_id = request.state.request_id
    start_time = time.time()
    
    try:
        predictions = []
        high_risk_count = 0
        
        for idx, merchant in enumerate(batch_request.merchants):
            input_data = merchant.model_dump()
            pred = predictor.predict(input_data, merchant_id=f"batch_{idx}")
            predictions.append(RiskPrediction(**pred))
            
            if pred["risk_label"] == "High Risk":
                high_risk_count += 1
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        logger.info(f"[{request_id}] Batch prediction: {len(predictions)} merchants, {high_risk_count} high risk")
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_processed=len(predictions),
            high_risk_count=high_risk_count,
            processing_time_ms=round(processing_time_ms, 2)
        )
    
    except Exception as e:
        log_error("BATCH_PREDICTION_ERROR", str(e), request_id)
        raise HTTPException(status_code=500, detail="Batch prediction failed")


@app.get("/model/info", tags=["Model"])
async def model_info():
    """
    Get model information and feature list.
    """
    if not predictor or not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Model not available")
    
    from .predict import FEATURE_COLUMNS, TOP_FEATURES
    
    return {
        "model_type": "XGBoost Classifier",
        "version": VERSION,
        "threshold": predictor.threshold,
        "num_features": len(FEATURE_COLUMNS),
        "top_features": [f[0] for f in TOP_FEATURES],
        "performance": {
            "roc_auc": 0.999,
            "recall": 0.923,
            "precision": 0.778,
            "f1_score": 0.844
        }
    }


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
