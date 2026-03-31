"""
Service layer – Model loading & prediction logic.

Uses pickle to load .pkl models as requested.
"""

import pickle
from pathlib import Path

import numpy as np

# ── Project root ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /CropRecommendationMP

# ── Model paths ──────────────────────────────────────────────────────────────
SVM_MODEL_PATH = BASE_DIR / "models" / "SVM_CropRecommendation.pkl"
RF_MODEL_PATH = BASE_DIR / "models" / "RFDiabetesv132.pkl"


def _load_model(path: Path):
    """Load a pickle model from disk. Raises FileNotFoundError if missing."""
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path.name}")
    with open(path, "rb") as file:
        model = pickle.load(file)
    return model


def prepare_features(N: int, P: int, K: int, temperature: float,
                     humidity: float, ph: float, rainfall: float) -> np.ndarray:
    """Convert individual feature values into a 2-D numpy array for sklearn."""
    return np.array([[N, P, K, temperature, humidity, ph, rainfall]])


def predict_with_svm(features: np.ndarray) -> str:
    """Run prediction using the SVM model."""
    model = _load_model(SVM_MODEL_PATH)
    prediction = model.predict(features)[0]
    return str(prediction)


def predict_with_rf(features: np.ndarray) -> str:
    """Run prediction using the Random Forest model."""
    model = _load_model(RF_MODEL_PATH)
    prediction = model.predict(features)[0]
    return str(prediction)
