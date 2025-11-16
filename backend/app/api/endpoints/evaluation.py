# backend/app/api/endpoints/evaluation.py

import logging
from fastapi import APIRouter, HTTPException, status

from ...models.evaluation_models import EvaluationRequest, EvaluationResponse
from ...services.ai_evaluator import evaluate_summary

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_summary_endpoint(request: EvaluationRequest):
    """
    Receives a transcript, summary, and evaluation parameters,
    gets an evaluation from an AI service, calculates a weighted score,
    and returns the detailed results.
    """
    if not request.transcript.strip() or not request.summary.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcript and summary cannot be empty."
        )
    
    if not request.parameters:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one evaluation parameter must be selected."
        )

    try:
        llm_result = await evaluate_summary(
            request.transcript,
            request.summary,
            request.parameters
        )

        # Calculate weighted score
        total_score = 0.0
        weights = request.weights or {param: 1 for param in request.parameters}
        total_weight = sum(weights.get(param, 1) for param in request.parameters)

        if total_weight == 0:
            final_score = 0.0
        else:
            for param, score in llm_result.scores.items():
                if param in request.parameters:
                    param_weight = weights.get(param, 1)
                    total_score += score * param_weight
            
            # Normalize the score to be out of 10
            final_score = (total_score / total_weight)

        return EvaluationResponse(
            scores=llm_result.scores,
            final_score=round(final_score, 2),
            explanation=llm_result.explanation
        )

    except Exception as e:
        logger.error(f"An error occurred during evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get evaluation from AI service. Error: {str(e)}"
        )
