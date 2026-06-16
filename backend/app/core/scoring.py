"""Funzioni pure di scoring (prezzo, distanza, servizi, punteggio finale).

Nessun I/O. Tutto deterministico e testabile.
"""

from __future__ import annotations

from app.core.decay import time_decay_score
from app.models.output import ComponentScores

NEUTRAL_SCORE = 50.0
# Punteggio prezzo: si parte da BASE al midpoint OMI e si toglie SLOPE punti
# per ogni punto percentuale sopra il midpoint (e viceversa sotto).
PRICE_BASE = 80.0
PRICE_SLOPE = 2.0


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def price_score(
    price_per_mq: float,
    omi_min: float | None,
    omi_max: float | None,
) -> tuple[float, float | None]:
    """Ritorna (punteggio 0..100, delta_pct_vs_mercato | None).

    Riferimento = midpoint OMI. Sotto il midpoint -> punteggio alto, sopra -> basso.
    Se i dati OMI mancano -> (NEUTRAL_SCORE, None): un dataset assente non premia
    né punisce.
    """
    if omi_min is None or omi_max is None:
        return NEUTRAL_SCORE, None
    midpoint = (omi_min + omi_max) / 2.0
    delta_pct = round((price_per_mq - midpoint) / midpoint * 100.0, 1)
    score = _clamp(PRICE_BASE - PRICE_SLOPE * delta_pct)
    return round(score, 1), delta_pct


def distance_score(
    metro_minutes: float | None,
    transit_minutes: float | None,
    w_metro: float = 0.6,
    w_transit: float = 0.4,
) -> float:
    """Blend pesato del decadimento su metro vs altri trasporti pubblici.

    Un input None significa "non trovato" -> contribuisce 0.
    """
    m = time_decay_score(metro_minutes) if metro_minutes is not None else 0.0
    t = time_decay_score(transit_minutes) if transit_minutes is not None else 0.0
    return round(w_metro * m + w_transit * t, 1)


def services_score(
    amenity_minutes: dict[str, float | None],
    preferences: dict[str, float],
) -> float:
    """Media pesata del decadimento per categoria, pesi = preferenze utente.

    Le categorie con peso 0 sono ignorate. Categoria non trovata (None) -> 0.
    """
    total_w = 0.0
    acc = 0.0
    for category, weight in preferences.items():
        if weight <= 0:
            continue
        minutes = amenity_minutes.get(category)
        score = time_decay_score(minutes) if minutes is not None else 0.0
        acc += weight * score
        total_w += weight
    if total_w == 0:
        return 0.0
    return round(acc / total_w, 1)


def final_score(components: ComponentScores, weights: dict[str, float]) -> float:
    """Somma pesata dei 4 componenti -> 0..100."""
    if abs(sum(weights.values()) - 1.0) > 1e-6:
        raise ValueError("i pesi devono sommare a 1.0")
    total = (
        components.price_score * weights["price"]
        + components.distance_score * weights["distance"]
        + components.services_score * weights["services"]
        + components.objective_score * weights["objective"]
    )
    return round(_clamp(total), 1)
