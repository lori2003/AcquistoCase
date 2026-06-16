import pytest

from app.core.objective import (
    COHERENCE_THRESHOLD,
    objective_score,
    objective_weights,
)
from app.models.input import ObjectiveType


def test_near_metro_uses_metro_decay():
    score, coherent = objective_score(ObjectiveType.near_metro, None, 5.0, {})
    assert score == 100.0
    assert coherent is True


def test_below_market_rewards_negative_delta():
    score, coherent = objective_score(ObjectiveType.below_market, -20.0, None, {})
    assert score == 90.0
    assert coherent is True


def test_nightlife_uses_bar_and_restaurant():
    amenity = {"bar": 5.0, "restaurant": 15.0}
    score, _ = objective_score(ObjectiveType.nightlife, None, None, amenity)
    assert score == 50.0  # media di 100 e 0


def test_family_uses_school_and_park():
    score, _ = objective_score(ObjectiveType.family, None, None, {"school": 5.0, "park": 5.0})
    assert score == 100.0


def test_near_center_uses_center_distance():
    score, coherent = objective_score(ObjectiveType.near_center, None, None, {"center": 5.0})
    assert score == 100.0
    assert coherent is True


def test_family_with_no_services_is_zero():
    score, coherent = objective_score(ObjectiveType.family, None, None, {})
    assert score == 0.0
    assert coherent is False


def test_below_market_with_missing_delta_is_neutral():
    score, _ = objective_score(ObjectiveType.below_market, None, None, {})
    assert score == 50.0


def test_future_value_blends_price_and_metro():
    # delta -20 -> price_part 90; metro 5 -> 100; blend 0.5/0.5 = 95
    score, _ = objective_score(ObjectiveType.future_value, -20.0, 5.0, {})
    assert score == 95.0


def test_coherence_threshold_boundary():
    # metro a 9 min -> decay 60 -> coerente (>= soglia)
    score, coherent = objective_score(ObjectiveType.near_metro, None, 9.0, {})
    assert score == 60.0 == COHERENCE_THRESHOLD
    assert coherent is True
    # metro a 9.1 min -> decay 59 -> non coerente
    score2, coherent2 = objective_score(ObjectiveType.near_metro, None, 9.1, {})
    assert score2 == 59.0
    assert coherent2 is False


@pytest.mark.parametrize("objective", list(ObjectiveType))
def test_weights_always_sum_to_one(objective):
    weights = objective_weights(objective)
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    assert all(w >= 0 for w in weights.values())


def test_near_metro_boosts_distance_weight():
    assert objective_weights(ObjectiveType.near_metro)["distance"] == 0.40


def test_below_market_boosts_price_weight():
    assert objective_weights(ObjectiveType.below_market)["price"] == 0.40
