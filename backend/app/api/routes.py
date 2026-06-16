"""Endpoint FastAPI (sottili)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_evaluation_service
from app.models.input import EvaluationRequest
from app.models.output import EvaluationResponse
from app.services.orchestrator import EvaluationService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
) -> EvaluationResponse:
    return service.evaluate(request)
