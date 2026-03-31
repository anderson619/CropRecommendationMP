"""
Pydantic v2 schemas – Crop Recommendation.
"""

from pydantic import BaseModel, Field


class CropInput(BaseModel):
    """Input schema: 7 soil & climate features required by both ML models."""

    N: int = Field(..., description="Ratio of Nitrogen content in soil", examples=[90])
    P: int = Field(..., description="Ratio of Phosphorous content in soil", examples=[42])
    K: int = Field(..., description="Ratio of Potassium content in soil", examples=[43])
    temperature: float = Field(
        ..., description="Temperature in degree Celsius", examples=[20.87]
    )
    humidity: float = Field(
        ..., description="Relative humidity in %%", examples=[82.0]
    )
    ph: float = Field(
        ..., description="pH value of the soil", examples=[6.5]
    )
    rainfall: float = Field(
        ..., description="Rainfall in mm", examples=[202.93]
    )


class PredictionResponse(BaseModel):
    """Unified response returned by every prediction endpoint."""

    prediction: str = Field(..., description="Recommended crop name")
    model_used: str = Field(..., description="Name of the ML model used")
