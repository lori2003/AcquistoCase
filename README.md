# AcquistoCase

Web app per principianti che aiuta a capire se una casa è in linea con il proprio
obiettivo di acquisto. L'utente inserisce i dati dell'immobile (città, indirizzo,
budget, prezzo, mq), un obiettivo personale e le sue preferenze sui servizi; l'app
restituisce un **punteggio da 0 a 100**, il confronto con i valori di mercato OMI,
la distanza a piedi da metro/trasporti, un punteggio di prossimità ai servizi, una
spiegazione in linguaggio semplice e l'elenco dei limiti/rischi dei dati.

## Stack

- **Backend**: FastAPI (Python). Logica di scoring in funzioni pure (`app/core`),
  servizi esterni dietro interfacce mockabili (`app/services`).
- **Frontend**: Next.js (React + TypeScript).
- **Fonti dati gratuite**: dati OMI (Agenzia delle Entrate, snapshot CSV),
  OpenStreetMap (Nominatim per il geocoding, Overpass per i servizi), opzionale
  OSMnx per il routing a piedi reale.
- **AI**: report testuale via OpenRouter (riceve solo dati strutturati, non inventa
  nulla; senza chiave si usa una sintesi locale di fallback).

## Struttura

```
backend/    # API FastAPI + logica di scoring + test (pytest, copertura 100% su core)
frontend/   # App Next.js + componenti + test (Vitest/RTL + e2e Playwright)
```

## Avvio in locale

Backend:

```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

Configura le variabili d'ambiente copiando `.env.example` (vedi le note nel file).
Le chiavi API non vanno mai messe nel codice.

## Test

```bash
# Backend: test + soglia di copertura
cd backend && pytest

# Frontend: unit + copertura, ed e2e
cd frontend && npm run test:cov && npm run test:e2e
```

La CI (`.github/workflows/ci.yml`) esegue entrambe le suite e applica le soglie di
copertura (backend ≥ 85%, frontend ≥ 80%) a ogni push e pull request.

## Note sui dati (da verificare manualmente prima di comprare)

- I valori OMI sono indicativi: controlla sempre la quotazione ufficiale sul sito
  dell'Agenzia delle Entrate.
- Le distanze dell'MVP sono stimate in linea d'aria convertite in minuti a piedi:
  la distanza reale può differire.
- I dati OpenStreetMap possono essere incompleti per alcune zone.
- Verifica sempre stato dell'immobile, classe energetica e spese condominiali.
