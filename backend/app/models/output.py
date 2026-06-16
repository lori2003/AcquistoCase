"""Modelli Pydantic di output (punteggi, contesto prezzo, report)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ComponentScores(BaseModel):
    price_score: float = Field(ge=0, le=100)
    distance_score: float = Field(ge=0, le=100)
    services_score: float = Field(ge=0, le=100)
    objective_score: float = Field(ge=0, le=100)


class PriceContext(BaseModel):
    price_per_mq: float
    omi_min_per_mq: float | None = None
    omi_max_per_mq: float | None = None
    delta_pct_vs_market: float | None = None  # negativo = sotto mercato
    data_available: bool = False


class AmenityHit(BaseModel):
    category: str
    name: str | None = None
    walk_minutes: float
    distance_m: float


class DataRisk(BaseModel):
    code: str  # es. "OMI_MISSING", "NO_AMENITIES", "AI_UNAVAILABLE"
    message: str


class EvaluationResponse(BaseModel):
    final_score: float = Field(ge=0, le=100)
    components: ComponentScores
    coherent_with_objective: bool
    price_context: PriceContext
    nearest_amenities: list[AmenityHit] = Field(default_factory=list)
    report_text: str
    data_risks: list[DataRisk] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
