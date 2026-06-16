"""Configurazione dell'app: legge SOLO da variabili d'ambiente.

Nessuna chiave segreta è mai scritta nel codice.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ACQUISTOCASE_", env_file=".env", extra="ignore")

    # Servizi esterni (tutti opzionali: senza chiave si usano i fallback)
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-4o-mini"
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    overpass_base_url: str = "https://overpass-api.de/api/interpreter"
    user_agent: str = "AcquistoCase/0.1 (https://github.com/lori2003/AcquistoCase)"

    # CORS per il frontend Next.js in sviluppo
    cors_origins: list[str] = ["http://localhost:3000"]


def get_settings() -> Settings:
    return Settings()
