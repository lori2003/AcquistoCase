import pytest
from pydantic import ValidationError

from app.models.input import EvaluationRequest, ObjectiveType, PropertyInput


def _valid_property(**overrides):
    base = dict(city="Milano", address="Via Roma 1", budget_eur=300000, price_eur=250000, mq=80)
    base.update(overrides)
    return base


def test_valid_property_passes():
    prop = PropertyInput(**_valid_property())
    assert prop.has_location()


def test_mq_zero_rejected():
    with pytest.raises(ValidationError):
        PropertyInput(**_valid_property(mq=0))


def test_negative_price_rejected():
    with pytest.raises(ValidationError):
        PropertyInput(**_valid_property(price_eur=-1))


def test_budget_zero_rejected():
    with pytest.raises(ValidationError):
        PropertyInput(**_valid_property(budget_eur=0))


def test_missing_location_rejected():
    data = _valid_property()
    data.pop("address")
    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_coordinates_count_as_location():
    data = _valid_property()
    data.pop("address")
    prop = PropertyInput(lat=45.46, lon=9.19, **data)
    assert prop.has_location()


def test_lat_out_of_range_rejected():
    with pytest.raises(ValidationError):
        PropertyInput(lat=200, lon=9.19, **{k: v for k, v in _valid_property().items() if k != "address"})


def test_full_request_builds():
    req = EvaluationRequest(property=PropertyInput(**_valid_property()), objective=ObjectiveType.near_metro)
    assert req.objective == ObjectiveType.near_metro
    assert req.preferences.metro == 0.5
