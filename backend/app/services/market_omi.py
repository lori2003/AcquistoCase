"""Provider dei valori di mercato OMI da uno snapshot CSV pubblico.

Sostituisce una API OMI pulita (che non esiste). I dati sono indicativi e vanno
verificati manualmente sul sito dell'Agenzia delle Entrate. Escluso dalla soglia
di copertura (I/O su file + dataset di esempio).
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.services.interfaces import OmiRange

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "omi_sample.csv"


class OmiCsvProvider:
    def __init__(self, csv_path: Path | None = None) -> None:
        self._rows = self._load(csv_path or _DATA_PATH)

    @staticmethod
    def _load(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def omi_range(self, city: str, zone: str | None) -> OmiRange:
        city_n = (city or "").strip().lower()
        zone_n = (zone or "").strip().lower()
        match = None
        fallback = None
        for row in self._rows:
            if row["city"].strip().lower() != city_n:
                continue
            row_zone = row["zone"].strip().lower()
            if row_zone == zone_n:
                match = row
                break
            if row_zone == "":
                fallback = row
        chosen = match or fallback
        if chosen is None:
            return OmiRange(min_per_mq=None, max_per_mq=None)
        return OmiRange(
            min_per_mq=float(chosen["omi_min_per_mq"]),
            max_per_mq=float(chosen["omi_max_per_mq"]),
        )
