from app.core.dedup import deduplicate, same_property
from app.models.listing import Listing


def _listing(source, price=250000, mq=80, lat=45.4655, lon=9.1715, city="Milano"):
    return Listing(
        id=f"{source}-{price}-{mq}",
        price_eur=price,
        mq=mq,
        price_per_mq=round(price / mq, 2),
        city=city,
        lat=lat,
        lon=lon,
        sources=[source],
    )


def test_same_property_within_tolerance():
    a = _listing("immobiliare", price=250000, mq=80, lat=45.4655, lon=9.1715)
    b = _listing("idealista", price=252000, mq=81, lat=45.4656, lon=9.1716)
    assert same_property(a, b) is True


def test_different_price_not_same():
    a = _listing("a", price=250000)
    b = _listing("b", price=400000)
    assert same_property(a, b) is False


def test_far_apart_not_same():
    a = _listing("a", lat=45.4655, lon=9.1715)
    b = _listing("b", lat=45.50, lon=9.25)
    assert same_property(a, b) is False


def test_falls_back_to_city_when_no_coords():
    a = _listing("a", lat=None, lon=None, city="Milano")
    b = _listing("b", lat=None, lon=None, city="Milano")
    assert same_property(a, b) is True


def test_deduplicate_merges_sources():
    a = _listing("immobiliare", price=250000, mq=80)
    b = _listing("idealista", price=252000, mq=81)
    c = _listing("immobiliare", price=400000, mq=120, lat=45.50, lon=9.25)
    result = deduplicate([a, b, c])
    assert len(result) == 2
    merged = next(r for r in result if r.price_eur == 250000)
    assert merged.sources == ["immobiliare", "idealista"]


def test_merge_completes_missing_fields():
    a = _listing("a")
    a.address = None
    b = _listing("b")
    b.address = "Via Vigevano 12"
    result = deduplicate([a, b])
    assert len(result) == 1
    assert result[0].address == "Via Vigevano 12"


def test_no_duplicates_preserves_all():
    a = _listing("a", price=100000, mq=50, lat=45.0, lon=9.0)
    b = _listing("b", price=300000, mq=90, lat=46.0, lon=10.0)
    assert len(deduplicate([a, b])) == 2
