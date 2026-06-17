"""Modello canonico di un annuncio immobiliare aggregato da più sorgenti."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Listing(BaseModel):
    id: str
    title: str | None = None
    price_eur: float = Field(gt=0)
    mq: float = Field(gt=0)
    price_per_mq: float = Field(ge=0)
    rooms: int | None = None
    address: str | None = None
    city: str
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)
    url: str | None = None
    image_url: str | None = None
    # Portali di provenienza dopo la deduplica, es. ["immobiliare", "idealista"]
    sources: list[str] = Field(default_factory=list)
