from app.core.scoring import NEUTRAL_SCORE, price_score


def test_below_midpoint_high_score_and_negative_delta():
    # midpoint = 2500, prezzo 2000 -> -20% -> score alto
    score, delta = price_score(2000, omi_min=2000, omi_max=3000)
    assert delta == -20.0
    assert score > 80.0


def test_above_max_is_low():
    # midpoint 2500, prezzo 3500 -> +40% -> score basso
    score, delta = price_score(3500, omi_min=2000, omi_max=3000)
    assert delta == 40.0
    assert score < 50.0


def test_at_midpoint_uses_base():
    score, delta = price_score(2500, omi_min=2000, omi_max=3000)
    assert delta == 0.0
    assert score == 80.0


def test_missing_omi_returns_neutral_and_none():
    assert price_score(2500, None, 3000) == (NEUTRAL_SCORE, None)
    assert price_score(2500, 2000, None) == (NEUTRAL_SCORE, None)


def test_score_is_clamped():
    # prezzo enormemente sopra mercato -> non scende sotto 0
    score, _ = price_score(100000, omi_min=2000, omi_max=3000)
    assert score == 0.0
