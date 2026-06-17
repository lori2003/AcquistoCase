from app.services.aggregator import AggregatorService
from app.services.listing_sources import SampleListingSource
from tests.fakes.fake_services import FakeListingSource

NAVIGLI_IMM = {
    "prezzo_vendita": "250.000 €",
    "superficie": "80 m²",
    "citta": "Milano",
    "latitudine": 45.4655,
    "longitudine": 9.1715,
}
NAVIGLI_IDE = {
    "price": 252000,
    "size": 81,
    "city": "Milano",
    "lat": 45.4656,
    "lng": 9.1716,
}
OTHER = {"price": 400000, "size": 120, "city": "Milano", "lat": 45.50, "lon": 9.25}


def test_aggregates_and_dedups_across_sources():
    service = AggregatorService(
        sources=[
            FakeListingSource("immobiliare", [NAVIGLI_IMM, OTHER]),
            FakeListingSource("idealista", [NAVIGLI_IDE]),
        ]
    )
    result = service.aggregate("Milano")
    assert len(result) == 2  # il Navigli è unito
    navigli = next(r for r in result if 79 <= r.mq <= 82)
    assert set(navigli.sources) == {"immobiliare", "idealista"}


def test_results_sorted_by_price_per_mq():
    service = AggregatorService(
        sources=[FakeListingSource("a", [NAVIGLI_IMM, OTHER])]
    )
    result = service.aggregate("Milano")
    prices = [r.price_per_mq for r in result]
    assert prices == sorted(prices)


def test_empty_when_no_listings():
    service = AggregatorService(sources=[FakeListingSource("a", [])])
    assert service.aggregate("Milano") == []


def test_sample_sources_merge_navigli_duplicate():
    # Usa i file JSON reali del repo: il Navigli compare in entrambi i portali.
    service = AggregatorService(
        sources=[
            SampleListingSource("immobiliare", "listings_immobiliare.json"),
            SampleListingSource("idealista", "listings_idealista.json"),
        ]
    )
    result = service.aggregate("Milano")
    navigli = [r for r in result if 79 <= r.mq <= 82]
    assert len(navigli) == 1
    assert set(navigli[0].sources) == {"immobiliare", "idealista"}


def test_sample_source_filters_by_city():
    src = SampleListingSource("idealista", "listings_idealista.json")
    assert all(r["city"] == "Roma" for r in src.fetch("Roma"))
