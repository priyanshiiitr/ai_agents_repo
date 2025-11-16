# backend/app/models/evaluation_models.py

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class EvaluationRequest(BaseModel):
    transcript: str = Field(..., description="The full text of the lecture or source material.")
    summary: str = Field(..., description="The student's summary of the transcript.")
    parameters: List[str] = Field(..., description="A list of criteria to evaluate the summary against.", min_items=1)
    weights: Optional[Dict[str, float]] = Field(None, description="Optional weights for each parameter for score calculation.")

class LLMResponse(BaseModel):
    """Defines the structure we expect back from the LLM."""
    scores: Dict[str, int]
    explanation: str

class EvaluationResponse(BaseModel):
    """The final response model sent back to the client."""
    scores: Dict[str, int] = Field(..., description="A dictionary of scores for each evaluation parameter.")
    final_score: float = Field(..., description="The final calculated (and possibly weighted) score.")
    explanation: str = Field(..., description="The qualitative feedback from the AI.")
