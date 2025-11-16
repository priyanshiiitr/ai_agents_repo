# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import evaluation
from .core.config import settings

app = FastAPI(title="Summary Evaluator API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(evaluation.router, prefix="/api/v1", tags=["evaluation"])

@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint for health check."""
    return {"status": "ok"}
