"""Orchestratore: chiama i servizi esterni, poi la logica pura `core`.

È volutamente sottile. Tutte le decisioni numeriche stanno in `app.core`.
"""

from __future__ import annotations

from app.core.objective import objective_score, objective_weights
from app.core.scoring import distance_score, final_score, price_score, services_score
from app.models.input import EvaluationRequest
from app.models.output import (
    ComponentScores,
    DataRisk,
    EvaluationResponse,
    PriceContext,
)
from app.services.interfaces import (
    AIReporter,
    AmenityProvider,
    Geocoder,
    MarketPriceProvider,
)

# Categorie OSM che recuperiamo. "center" = distanza dal centro città.
CATEGORIES = [
    "metro",
    "public_transport",
    "supermarket",
    "school",
    "bar",
    "restaurant",
    "park",
    "center",
]


def _prefs_to_categories(prefs: dict[str, float]) -> dict[str, float]:
    """Allinea le chiavi delle preferenze alle categorie amenity."""
    mapping = dict(prefs)
    mapping["center"] = mapping.pop("distance_center")
    return mapping


def _fallback_report(final: float, coherent: bool) -> str:
    coerenza = "in linea" if coherent else "non del tutto in linea"
    return (
        f"Valutazione automatica: punteggio complessivo {final}/100. "
        f"L'immobile risulta {coerenza} con l'obiettivo dichiarato. "
        "Report AI non disponibile: questa è una sintesi generata localmente dai dati calcolati."
    )


def _suggestions(risks: list[DataRisk], coherent: bool) -> list[str]:
    out: list[str] = []
    if not coherent:
        out.append("Confronta con altri immobili: questo non massimizza il tuo obiettivo.")
    codes = {r.code for r in risks}
    if "OMI_MISSING" in codes:
        out.append("Verifica manualmente i valori OMI sul sito dell'Agenzia delle Entrate.")
    if "NO_AMENITIES" in codes:
        out.append("Controlla di persona la presenza di servizi: i dati OSM erano insufficienti.")
    out.append("Verifica sempre stato, classe energetica e spese condominiali prima di acquistare.")
    return out


class EvaluationService:
    def __init__(
        self,
        geocoder: Geocoder,
        amenities: AmenityProvider,
        market: MarketPriceProvider,
        ai: AIReporter,
    ) -> None:
        self.geocoder = geocoder
        self.amenities = amenities
        self.market = market
        self.ai = ai

    def evaluate(self, request: EvaluationRequest) -> EvaluationResponse:
        prop = request.property
        risks: list[DataRisk] = []

        point = self.geocoder.geocode(
            address=prop.address, city=prop.city, lat=prop.lat, lon=prop.lon
        )

        hits = self.amenities.nearest_by_category(point, CATEGORIES)
        amenity_minutes = {cat: (hit.walk_minutes if hit else None) for cat, hit in hits.items()}
        if all(v is None for v in amenity_minutes.values()):
            risks.append(
                DataRisk(code="NO_AMENITIES", message="Nessun servizio trovato nei dati OpenStreetMap.")
            )

        omi = self.market.omi_range(prop.city, prop.zone)
        price_per_mq = prop.price_eur / prop.mq
        p_score, delta = price_score(price_per_mq, omi.min_per_mq, omi.max_per_mq)
        if omi.min_per_mq is None or omi.max_per_mq is None:
            risks.append(
                DataRisk(code="OMI_MISSING", message="Valori di mercato OMI non disponibili per questa zona.")
            )

        d_score = distance_score(amenity_minutes.get("metro"), amenity_minutes.get("public_transport"))
        s_score = services_score(amenity_minutes, _prefs_to_categories(request.preferences.model_dump()))
        o_score, coherent = objective_score(
            request.objective, delta, amenity_minutes.get("metro"), amenity_minutes
        )

        components = ComponentScores(
            price_score=p_score, distance_score=d_score, services_score=s_score, objective_score=o_score
        )
        weights = objective_weights(request.objective)
        final = final_score(components, weights)

        structured = {
            "final_score": final,
            "components": components.model_dump(),
            "coherent_with_objective": coherent,
            "objective": request.objective.value,
            "price_per_mq": round(price_per_mq, 2),
            "omi_min_per_mq": omi.min_per_mq,
            "omi_max_per_mq": omi.max_per_mq,
            "delta_pct_vs_market": delta,
            "amenity_minutes": amenity_minutes,
        }
        ai_result = self.ai.write_report(structured)
        if ai_result.ok and ai_result.text:
            report_text = ai_result.text
        else:
            report_text = _fallback_report(final, coherent)
            risks.append(
                DataRisk(code="AI_UNAVAILABLE", message="Report AI non disponibile: usata una sintesi locale.")
            )

        price_context = PriceContext(
            price_per_mq=round(price_per_mq, 2),
            omi_min_per_mq=omi.min_per_mq,
            omi_max_per_mq=omi.max_per_mq,
            delta_pct_vs_market=delta,
            data_available=omi.min_per_mq is not None and omi.max_per_mq is not None,
        )
        nearest = [hit for hit in hits.values() if hit is not None]

        return EvaluationResponse(
            final_score=final,
            components=components,
            coherent_with_objective=coherent,
            price_context=price_context,
            nearest_amenities=nearest,
            report_text=report_text,
            data_risks=risks,
            suggestions=_suggestions(risks, coherent),
        )
