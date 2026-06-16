from app.core.scoring import services_score


def test_no_amenities_found_is_zero():
    amenity_minutes = {"bar": None, "park": None}
    prefs = {"bar": 1.0, "park": 1.0}
    assert services_score(amenity_minutes, prefs) == 0.0


def test_zero_weight_excludes_category():
    # park ottimo ma peso 0 -> ignorato; conta solo bar (lontano -> 0)
    amenity_minutes = {"bar": 20.0, "park": 5.0}
    prefs = {"bar": 1.0, "park": 0.0}
    assert services_score(amenity_minutes, prefs) == 0.0


def test_normalization_with_unbalanced_weights():
    # bar a 5 min (100), park a 15 min (0); pesi 3:1 -> media pesata 75
    amenity_minutes = {"bar": 5.0, "park": 15.0}
    prefs = {"bar": 0.75, "park": 0.25}
    assert services_score(amenity_minutes, prefs) == 75.0


def test_all_weights_zero_returns_zero():
    assert services_score({"bar": 5.0}, {"bar": 0.0}) == 0.0


def test_single_category_full():
    assert services_score({"metro": 5.0}, {"metro": 0.5}) == 100.0
