"""Normalizzatore (Transformer): mappa annunci grezzi eterogenei nel modello canonico.

Funzioni pure: ogni portale chiama i campi in modo diverso (prezzo_vendita / price /
costo, mq / superficie / size...), qui tutto confluisce in un unico `Listing`.
"""

from __future__ import annotations

import hashlib

from app.models.listing import Listing

# Alias dei campi per ciascuna proprietà canonica (ordine = priorità)
PRICE_KEYS = ["price_eur", "price", "prezzo", "prezzo_vendita", "costo"]
MQ_KEYS = ["mq", "superficie", "size", "square_meters", "sqm", "metri_quadri"]
ROOMS_KEYS = ["rooms", "locali", "vani", "stanze"]
TITLE_KEYS = ["title", "titolo", "name", "descrizione_breve"]
ADDRESS_KEYS = ["address", "indirizzo", "via"]
CITY_KEYS = ["city", "citta", "città", "comune"]
LAT_KEYS = ["lat", "latitude", "latitudine"]
LON_KEYS = ["lon", "lng", "longitude", "longitudine"]
URL_KEYS = ["url", "link", "permalink"]
IMAGE_KEYS = ["image_url", "image", "thumbnail", "foto"]


def _first(raw: dict, keys: list[str]):
    for k in keys:
        if k in raw and raw[k] not in (None, ""):
            return raw[k]
    return None


def _to_float(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    # gestisce "250.000 €", "1.250,50", "120 m²"
    cleaned = (
        str(value)
        .replace("€", "")
        .replace("m²", "")
        .replace("mq", "")
        .replace(" ", "")
        .strip()
    )
    if "," in cleaned and "." in cleaned:
        # formato italiano "1.250,50" -> il punto è separatore migliaia
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    elif "." in cleaned and len(cleaned.rsplit(".", 1)[1]) == 3:
        # solo punti con ultimo gruppo di 3 cifre ("250.000") -> migliaia
        cleaned = cleaned.replace(".", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def _make_id(source: str, price: float, mq: float, lat, lon) -> str:
    seed = f"{source}|{round(price)}|{round(mq)}|{lat}|{lon}"
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]


def normalize_listing(raw: dict, source: str) -> Listing:
    """Trasforma un annuncio grezzo nel modello canonico.

    Solleva ValueError se mancano prezzo, mq o città (campi essenziali).
    """
    price = _to_float(_first(raw, PRICE_KEYS))
    mq = _to_float(_first(raw, MQ_KEYS))
    city = _first(raw, CITY_KEYS)
    if not price or price <= 0:
        raise ValueError("prezzo mancante o non valido")
    if not mq or mq <= 0:
        raise ValueError("mq mancante o non valido")
    if not city:
        raise ValueError("città mancante")

    lat = _to_float(_first(raw, LAT_KEYS))
    lon = _to_float(_first(raw, LON_KEYS))
    rooms_raw = _to_float(_first(raw, ROOMS_KEYS))

    return Listing(
        id=_make_id(source, price, mq, lat, lon),
        title=_first(raw, TITLE_KEYS),
        price_eur=price,
        mq=mq,
        price_per_mq=round(price / mq, 2),
        rooms=int(rooms_raw) if rooms_raw else None,
        address=_first(raw, ADDRESS_KEYS),
        city=str(city),
        lat=lat,
        lon=lon,
        url=_first(raw, URL_KEYS),
        image_url=_first(raw, IMAGE_KEYS),
        sources=[source],
    )


def normalize_many(raws: list[dict], source: str) -> list[Listing]:
    """Normalizza una lista, scartando silenziosamente gli annunci non validi."""
    out: list[Listing] = []
    for raw in raws:
        try:
            out.append(normalize_listing(raw, source))
        except ValueError:
            continue
    return out
