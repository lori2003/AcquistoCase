from app.models.input import EvaluationRequest, ObjectiveType, PropertyInput


def _request(objective=ObjectiveType.near_metro, **prop_overrides):
    base = dict(city="Milano", address="Via Roma 1", budget_eur=300000, price_eur=200000, mq=80)
    base.update(prop_overrides)
    return EvaluationRequest(property=PropertyInput(**base), objective=objective)


def test_full_response_assembled(make_service):
    service = make_service(amenities={"metro": 5.0, "bar": 5.0, "restaurant": 5.0})
    resp = service.evaluate(_request())
    assert 0 <= resp.final_score <= 100
    assert resp.report_text == "Report AI di prova."
    assert resp.data_risks == []
    assert any(a.category == "metro" for a in resp.nearest_amenities)


def test_missing_omi_raises_risk_and_neutral_price(make_service):
    service = make_service(amenities={"metro": 5.0}, omi_min=None, omi_max=None)
    resp = service.evaluate(_request())
    assert resp.components.price_score == 50.0
    assert resp.price_context.data_available is False
    assert any(r.code == "OMI_MISSING" for r in resp.data_risks)


def test_no_amenities_raises_risk(make_service):
    service = make_service(amenities={})  # nessun servizio trovato
    resp = service.evaluate(_request())
    assert any(r.code == "NO_AMENITIES" for r in resp.data_risks)
    assert resp.components.distance_score == 0.0


def test_ai_failure_uses_fallback_but_still_scores(make_service):
    service = make_service(amenities={"metro": 5.0}, ai_fail=True)
    resp = service.evaluate(_request())
    assert any(r.code == "AI_UNAVAILABLE" for r in resp.data_risks)
    assert "sintesi generata localmente" in resp.report_text
    assert 0 <= resp.final_score <= 100


def test_below_market_price_scores_well(make_service):
    # prezzo 2000/mq con OMI 4000-6000 -> molto sotto mercato
    service = make_service(amenities={"metro": 5.0}, omi_min=4000.0, omi_max=6000.0)
    resp = service.evaluate(_request(objective=ObjectiveType.below_market, price_eur=160000, mq=80))
    assert resp.price_context.delta_pct_vs_market < 0
    assert resp.components.price_score == 100.0
