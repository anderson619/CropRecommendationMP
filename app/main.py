"""
Crop Recommendation API – FastAPI entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routes.cropRecommendation_router import router as crop_router

app = FastAPI(
    title="Crop Recommendation API",
    description=(
        "API de producción para recomendación de cultivos "
        "basada en modelos SVM y Random Forest pre-entrenados."
    ),
    version="1.0.0",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(crop_router)

# ── Static files (CSS, JS, assets) ──────────────────────────────────────────
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Root – JSON response for Postman / health checks ────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Returns a JSON welcome message (visible in Postman)."""
    return {
        "message": "Crop Recommendation API is running 🌱",
        "endpoints": ["/predict/svm", "/predict/rf"],
    }


# ── Frontend – served at /app ───────────────────────────────────────────────
@app.get("/app", include_in_schema=False)
async def serve_frontend():
    """Serve the single-page frontend at /app."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Frontend not found. Place index.html in /static/"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
