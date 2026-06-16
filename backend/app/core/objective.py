"""Logica pura legata all'obiettivo dichiarato dall'utente.

Mappa l'obiettivo sui segnali rilevanti (coerenza) e sui pesi dei componenti.
"""

from __future__ import annotations

from app.core.decay import time_decay_score
from app.models.input import ObjectiveType

COHERENCE_THRESHOLD = 60.0

# Pesi base dei 4 componenti (sommano a 1.0). Enfasi su distanza, prezzo e obiettivo.
BASE_WEIGHTS: dict[str, float] = {
    "price": 0.30,
    "distance": 0.30,
    "services": 0.15,
    "objective": 0.25,
}


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _decay_or_zero(minutes: float | None) -> float:
    return time_decay_score(minutes) if minutes is not None else 0.0


def _avg_decay(minutes_list: list[float | None]) -> float:
    values = [time_decay_score(m) for m in minutes_list if m is not None]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)


def _below_market_score(price_delta_pct: float | None) -> float:
    if price_delta_pct is None:
        return 50.0
    # delta negativo (sotto mercato) -> punteggio alto
    return _clamp(50.0 - 2.0 * price_delta_pct)


def objective_score(
    objective: ObjectiveType,
    price_delta_pct: float | None,
    metro_minutes: float | None,
    amenity_minutes: dict[str, float | None],
) -> tuple[float, bool]:
    """Ritorna (punteggio 0..100, coerente: bool) per l'obiettivo dichiarato."""
    if objective == ObjectiveType.near_metro:
        score = _decay_or_zero(metro_minutes)
    elif objective == ObjectiveType.below_market:
        score = _below_market_score(price_delta_pct)
    elif objective == ObjectiveType.nightlife:
        score = _avg_decay([amenity_minutes.get("bar"), amenity_minutes.get("restaurant")])
    elif objective == ObjectiveType.near_center:
        score = _decay_or_zero(amenity_minutes.get("center"))
    elif objective == ObjectiveType.family:
        score = _avg_decay([amenity_minutes.get("school"), amenity_minutes.get("park")])
    else:  # future_value: blend prezzo + accessibilità metro come proxy di desiderabilità
        price_part = _below_market_score(price_delta_pct)
        score = round(0.5 * price_part + 0.5 * _decay_or_zero(metro_minutes), 1)
    score = round(score, 1)
    return score, score >= COHERENCE_THRESHOLD


def objective_weights(objective: ObjectiveType) -> dict[str, float]:
    """Pesi dei 4 componenti, ribilanciati verso il segnale dell'obiettivo.

    Ritorna sempre pesi che sommano a 1.0.
    """
    w = dict(BASE_WEIGHTS)
    if objective == ObjectiveType.near_metro:
        w["distance"] += 0.10
        w["services"] -= 0.10
    elif objective == ObjectiveType.below_market:
        w["price"] += 0.10
        w["services"] -= 0.10
    elif objective == ObjectiveType.nightlife:
        w["services"] += 0.10
        w["price"] -= 0.10
    elif objective == ObjectiveType.near_center:
        w["distance"] += 0.10
        w["services"] -= 0.10
    elif objective == ObjectiveType.family:
        w["services"] += 0.10
        w["price"] -= 0.10
    # future_value: pesi base
    return w
