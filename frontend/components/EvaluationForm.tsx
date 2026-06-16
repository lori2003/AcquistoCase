"use client";

import { useState } from "react";
import { evaluate } from "@/lib/api-client";
import type { EvaluationResponse, ObjectiveType } from "@/lib/types";

const OBJECTIVES: { value: ObjectiveType; label: string }[] = [
  { value: "near_metro", label: "Vicino alla metro" },
  { value: "future_value", label: "Massimizzare il valore futuro" },
  { value: "nightlife", label: "Vicino a bar e ristoranti" },
  { value: "below_market", label: "Sotto il prezzo medio di zona" },
  { value: "near_center", label: "Vicino al centro" },
  { value: "family", label: "Scuole e parchi (famiglia)" },
];

export function EvaluationForm({
  onResult,
}: {
  onResult: (result: EvaluationResponse) => void;
}) {
  const [city, setCity] = useState("");
  const [address, setAddress] = useState("");
  const [budget, setBudget] = useState("");
  const [price, setPrice] = useState("");
  const [mq, setMq] = useState("");
  const [objective, setObjective] = useState<ObjectiveType>("near_metro");
  const [metro, setMetro] = useState(0.5);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!city.trim() || !address.trim()) {
      setError("Inserisci città e indirizzo.");
      return;
    }
    if (Number(mq) <= 0) {
      setError("I metri quadri devono essere maggiori di zero.");
      return;
    }
    if (Number(price) <= 0 || Number(budget) <= 0) {
      setError("Budget e prezzo devono essere maggiori di zero.");
      return;
    }
    setLoading(true);
    try {
      const result = await evaluate({
        property: {
          city,
          address,
          budget_eur: Number(budget),
          price_eur: Number(price),
          mq: Number(mq),
        },
        objective,
        preferences: { metro },
      });
      onResult(result);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} aria-label="Dati immobile">
      <label>
        Città
        <input value={city} onChange={(e) => setCity(e.target.value)} />
      </label>
      <label>
        Indirizzo
        <input value={address} onChange={(e) => setAddress(e.target.value)} />
      </label>
      <label>
        Budget (€)
        <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} />
      </label>
      <label>
        Prezzo (€)
        <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
      </label>
      <label>
        Metri quadri
        <input type="number" value={mq} onChange={(e) => setMq(e.target.value)} />
      </label>
      <label>
        Obiettivo
        <select
          value={objective}
          onChange={(e) => setObjective(e.target.value as ObjectiveType)}
        >
          {OBJECTIVES.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Importanza metro
        <input
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={metro}
          onChange={(e) => setMetro(Number(e.target.value))}
        />
      </label>

      {error && <p role="alert">{error}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Calcolo…" : "Valuta immobile"}
      </button>
    </form>
  );
}
