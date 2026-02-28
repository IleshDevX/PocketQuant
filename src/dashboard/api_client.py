"""
API Client for PocketQuant Dashboard.
Handles communication with the FastAPI backend.
"""
import requests
from typing import Dict, Any, Optional, List
from .config import API_BASE_URL


class RiskAPIClient:
    """Client for interacting with the PocketQuant Risk API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}
    
    def predict_risk(self, merchant_data: Dict[str, Any], merchant_id: str = None) -> Dict[str, Any]:
        """Get risk prediction for a single merchant."""
        try:
            params = {"merchant_id": merchant_id} if merchant_id else {}
            response = self.session.post(
                f"{self.base_url}/predict-risk",
                json=merchant_data,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def predict_batch(self, merchants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get risk predictions for multiple merchants."""
        try:
            response = self.session.post(
                f"{self.base_url}/predict-risk/batch",
                json={"merchants": merchants},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        try:
            response = self.session.get(f"{self.base_url}/model/info", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def get_api_client() -> RiskAPIClient:
    """Get singleton API client instance."""
    return RiskAPIClient()
