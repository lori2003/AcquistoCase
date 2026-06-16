"""Funzioni pure per il decadimento del punteggio con la distanza/tempo.

Nessun I/O: ogni funzione qui è deterministica e testabile al 100%.
"""

from __future__ import annotations

WALK_SPEED_M_PER_MIN = 80.0  # ~4.8 km/h, andatura a piedi media


def walk_minutes(distance_m: float, walk_speed_m_per_min: float = WALK_SPEED_M_PER_MIN) -> float:
    """Converte una distanza in metri in minuti a piedi.

    >>> walk_minutes(400)
    5.0
    """
    if distance_m < 0:
        raise ValueError("distance_m non può essere negativa")
    if walk_speed_m_per_min <= 0:
        raise ValueError("walk_speed_m_per_min deve essere > 0")
    return distance_m / walk_speed_m_per_min


def time_decay_score(minutes: float, full_until: float = 5.0, zero_after: float = 15.0) -> float:
    """Punteggio 0..100 in funzione dei minuti a piedi (decadimento lineare a tratti).

    Contratto di confine: f(5)=100, f(10)=50, f(15)=0.

    - minutes <= full_until      -> 100
    - full_until < m < zero_after -> lineare 100 -> 0
    - minutes >= zero_after      -> 0
    """
    if minutes < 0:
        raise ValueError("minutes non può essere negativo")
    if zero_after <= full_until:
        raise ValueError("zero_after deve essere > full_until")
    if minutes <= full_until:
        return 100.0
    if minutes >= zero_after:
        return 0.0
    frac = (minutes - full_until) / (zero_after - full_until)
    return round(100.0 * (1.0 - frac), 1)
