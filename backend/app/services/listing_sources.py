"""Sorgenti di annunci (Worker) dietro un'interfaccia collegabile.

Ogni sorgente restituisce annunci GREZZI (dict con i nomi-campo del portale).
La normalizzazione e la deduplica avvengono a valle, nel core.

NOTA IMPORTANTE: qui NON è incluso alcuno scraper che aggira protezioni anti-bot,
CAPTCHA o fingerprinting: raccogliere annunci da portali che lo vietano nei ToS è
un rischio legale. `SampleListingSource` usa dati di esempio/feed autorizzati; per
collegare una fonte reale, implementa `ListingSource.fetch` con una API ufficiale.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol, runtime_checkable

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@runtime_checkable
class ListingSource(Protocol):
    name: str

    def fetch(self, city: str) -> list[dict]: ...


class SampleListingSource:
    """Sorgente di esempio: legge annunci grezzi da un file JSON del repo."""

    def __init__(self, name: str, filename: str) -> None:
        self.name = name
        self._path = _DATA_DIR / filename

    def fetch(self, city: str) -> list[dict]:
        with self._path.open(encoding="utf-8") as f:
            raws = json.load(f)
        city_n = city.strip().lower()
        return [
            r
            for r in raws
            if str(r.get("city") or r.get("citta") or r.get("città") or "").strip().lower()
            == city_n
        ]
