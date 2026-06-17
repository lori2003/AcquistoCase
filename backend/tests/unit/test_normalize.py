import pytest

from app.core.normalize import normalize_listing, normalize_many


def test_maps_italian_field_names():
    raw = {
        "titolo": "Trilocale",
        "prezzo_vendita": "250.000 €",
        "superficie": "80 m²",
        "locali": 3,
        "citta": "Milano",
        "indirizzo": "Via Roma 1",
        "latitudine": 45.46,
        "longitudine": 9.19,
    }
    listing = normalize_listing(raw, "immobiliare")
    assert listing.price_eur == 250000.0
    assert listing.mq == 80.0
    assert listing.price_per_mq == 3125.0
    assert listing.rooms == 3
    assert listing.city == "Milano"
    assert listing.sources == ["immobiliare"]


def test_maps_english_field_names():
    raw = {"title": "Flat", "price": 200000, "size": 50, "city": "Roma", "lat": 41.9, "lng": 12.5}
    listing = normalize_listing(raw, "idealista")
    assert listing.price_eur == 200000.0
    assert listing.mq == 50.0
    assert listing.lon == 12.5


def test_parses_italian_decimal_format():
    raw = {"price": "1.250,50", "mq": 50, "city": "Milano"}
    listing = normalize_listing(raw, "x")
    assert listing.price_eur == 1250.50


def test_parses_thousands_dot_separator():
    raw = {"price": "250.000", "mq": 80, "city": "Milano"}
    listing = normalize_listing(raw, "x")
    assert listing.price_eur == 250000.0


def test_keeps_plain_decimal_point():
    raw = {"price": 100000, "mq": "62.5", "city": "Milano"}
    listing = normalize_listing(raw, "x")
    assert listing.mq == 62.5


def test_missing_price_raises():
    with pytest.raises(ValueError):
        normalize_listing({"mq": 80, "city": "Milano"}, "x")


def test_missing_mq_raises():
    with pytest.raises(ValueError):
        normalize_listing({"price": 100000, "city": "Milano"}, "x")


def test_missing_city_raises():
    with pytest.raises(ValueError):
        normalize_listing({"price": 100000, "mq": 80}, "x")


def test_normalize_many_skips_invalid():
    raws = [
        {"price": 100000, "mq": 50, "city": "Milano"},
        {"price": 0, "mq": 50, "city": "Milano"},  # scartato
        {"mq": 50, "city": "Milano"},  # scartato
    ]
    result = normalize_many(raws, "x")
    assert len(result) == 1


def test_same_input_same_id():
    raw = {"price": 100000, "mq": 50, "city": "Milano", "lat": 45.0, "lon": 9.0}
    assert normalize_listing(raw, "a").id == normalize_listing(raw, "a").id
