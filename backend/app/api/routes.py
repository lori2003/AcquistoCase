"""Endpoint FastAPI (sottili)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_aggregator_service, get_evaluation_service
from app.models.input import EvaluationRequest
from app.models.listing import Listing
from app.models.output import EvaluationResponse
from app.services.aggregator import AggregatorService
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


@router.get("/listings", response_model=list[Listing])
def listings(
    city: str,
    service: AggregatorService = Depends(get_aggregator_service),
) -> list[Listing]:
    return service.aggregate(city)
