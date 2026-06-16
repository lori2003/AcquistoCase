from app.core.scoring import distance_score


def test_metro_close_dominates():
    # metro a 5 min -> decay 100, peso 0.6
    assert distance_score(metro_minutes=5, transit_minutes=None) == 60.0


def test_both_none_is_zero():
    assert distance_score(None, None) == 0.0


def test_metro_weighted_more_than_transit():
    only_metro = distance_score(metro_minutes=5, transit_minutes=None)
    only_transit = distance_score(metro_minutes=None, transit_minutes=5)
    assert only_metro > only_transit


def test_both_present_full_score():
    assert distance_score(metro_minutes=5, transit_minutes=5) == 100.0
