"""Report testuale via OpenRouter.

Riceve SOLO dati strutturati e impone all'AI di non inventare nulla e di segnalare
quando i dati sono insufficienti. La chiave vive solo in env var. Se la chiave manca
o la chiamata fallisce, ritorna ok=False e l'orchestrator usa il fallback locale.
Escluso dalla soglia di copertura (codice di rete).
"""

from __future__ import annotations

import json

import httpx

from app.config import Settings
from app.services.interfaces import AIResult

SYSTEM_PROMPT = (
    "Sei un assistente che valuta immobili in Italia per un principiante. "
    "Usa ESCLUSIVAMENTE i dati forniti nel JSON: non inventare prezzi, distanze o servizi. "
    "Se un dato è null o mancante, dichiara esplicitamente che è insufficiente. "
    "Spiega in italiano semplice perché l'immobile è consigliato o sconsigliato, "
    "cita il punteggio finale e i punti deboli. Massimo 150 parole."
)


class OpenRouterReporter:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model

    def write_report(self, structured: dict) -> AIResult:
        if not self._api_key:
            return AIResult(ok=False, text=None)
        try:
            resp = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": json.dumps(structured, ensure_ascii=False)},
                    ],
                },
                timeout=30.0,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            return AIResult(ok=True, text=text)
        except (httpx.HTTPError, KeyError, IndexError):
            return AIResult(ok=False, text=None)
