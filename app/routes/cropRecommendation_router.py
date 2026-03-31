"""
Endpoints – Crop Recommendation Router.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.cropRecommendation_schema import CropInput, PredictionResponse
from app.services.cropRecommendation_service import (
    prepare_features,
    predict_with_svm,
    predict_with_rf,
)

router = APIRouter(prefix="/predict", tags=["Predictions"])


# ── POST /predict/svm ────────────────────────────────────────────────────────
@router.post("/svm", response_model=PredictionResponse, summary="Predict with SVM")
async def predict_svm(data: CropInput):
    """Return a crop recommendation using the **SVM** model."""
    try:
        features = prepare_features(
            data.N, data.P, data.K,
            data.temperature, data.humidity, data.ph, data.rainfall,
        )
        prediction = predict_with_svm(features)
        return PredictionResponse(prediction=prediction, model_used="SVM")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"SVM prediction error: {exc}") from exc


# ── POST /predict/rf ──────────────────────────────────────────────────────────
@router.post("/rf", response_model=PredictionResponse, summary="Predict with Random Forest")
async def predict_rf(data: CropInput):
    """Return a crop recommendation using the **Random Forest** model."""
    try:
        features = prepare_features(
            data.N, data.P, data.K,
            data.temperature, data.humidity, data.ph, data.rainfall,
        )
        prediction = predict_with_rf(features)
        return PredictionResponse(prediction=prediction, model_used="Random Forest")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RF prediction error: {exc}") from exc
