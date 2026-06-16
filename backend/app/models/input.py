"""Modelli Pydantic di input (immobile, obiettivo, preferenze)."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ObjectiveType(str, Enum):
    near_metro = "near_metro"        # "voglio una casa vicino alla metro"
    future_value = "future_value"    # "voglio massimizzare il valore futuro"
    nightlife = "nightlife"          # "voglio vivere vicino a bar e ristoranti"
    below_market = "below_market"    # "voglio comprare sotto il prezzo medio di zona"
    near_center = "near_center"      # "voglio vivere vicino al centro"
    family = "family"                # scuole + parchi


class ServicePreferences(BaseModel):
    """Importanza 0..1 che l'utente assegna a ciascun servizio (default neutro)."""

    metro: float = Field(0.5, ge=0, le=1)
    supermarket: float = Field(0.5, ge=0, le=1)
    school: float = Field(0.5, ge=0, le=1)
    bar: float = Field(0.5, ge=0, le=1)
    restaurant: float = Field(0.5, ge=0, le=1)
    park: float = Field(0.5, ge=0, le=1)
    public_transport: float = Field(0.5, ge=0, le=1)
    distance_center: float = Field(0.5, ge=0, le=1)


class PropertyInput(BaseModel):
    city: str = Field(min_length=1)
    zone: str | None = None
    address: str | None = None
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)
    budget_eur: float = Field(gt=0)
    price_eur: float = Field(gt=0)
    mq: float = Field(gt=0)

    @model_validator(mode="after")
    def location_present(self) -> "PropertyInput":
        if not self.has_location():
            raise ValueError("serve l'indirizzo oppure le coordinate (lat, lon)")
        return self

    def has_location(self) -> bool:
        return self.address is not None or (self.lat is not None and self.lon is not None)


class EvaluationRequest(BaseModel):
    property: PropertyInput
    objective: ObjectiveType
    preferences: ServicePreferences = ServicePreferences()
