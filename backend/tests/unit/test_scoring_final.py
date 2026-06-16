import pytest

from app.core.objective import objective_weights
from app.core.scoring import final_score
from app.models.input import ObjectiveType
from app.models.output import ComponentScores


def _components(p, d, s, o):
    return ComponentScores(price_score=p, distance_score=d, services_score=s, objective_score=o)


def test_all_100_gives_100():
    weights = objective_weights(ObjectiveType.future_value)
    assert final_score(_components(100, 100, 100, 100), weights) == 100.0


def test_weighted_sum_is_correct():
    weights = {"price": 0.30, "distance": 0.30, "services": 0.15, "objective": 0.25}
    # 80*.3 + 60*.3 + 40*.15 + 100*.25 = 24 + 18 + 6 + 25 = 73
    assert final_score(_components(80, 60, 40, 100), weights) == 73.0


def test_rejects_weights_not_summing_to_one():
    with pytest.raises(ValueError):
        final_score(_components(50, 50, 50, 50), {"price": 1, "distance": 1, "services": 1, "objective": 1})


def test_result_within_range():
    weights = objective_weights(ObjectiveType.near_metro)
    result = final_score(_components(0, 0, 0, 0), weights)
    assert 0.0 <= result <= 100.0
