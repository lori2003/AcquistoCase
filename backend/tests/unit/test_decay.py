import pytest

from app.core.decay import time_decay_score, walk_minutes


@pytest.mark.parametrize(
    "minutes, expected",
    [(0, 100.0), (5, 100.0), (10, 50.0), (15, 0.0), (20, 0.0)],
)
def test_decay_boundaries(minutes, expected):
    assert time_decay_score(minutes) == expected


def test_decay_is_monotonic_non_increasing():
    scores = [time_decay_score(m) for m in range(0, 21)]
    assert all(a >= b for a, b in zip(scores, scores[1:]))


def test_walk_minutes_conversion():
    assert walk_minutes(400) == 5.0
    assert walk_minutes(800) == 10.0


def test_walk_minutes_rejects_negative():
    with pytest.raises(ValueError):
        walk_minutes(-1)


def test_decay_rejects_bad_bounds():
    with pytest.raises(ValueError):
        time_decay_score(5, full_until=10, zero_after=5)


def test_decay_rejects_negative_minutes():
    with pytest.raises(ValueError):
        time_decay_score(-1)


def test_walk_minutes_rejects_zero_speed():
    with pytest.raises(ValueError):
        walk_minutes(100, walk_speed_m_per_min=0)
