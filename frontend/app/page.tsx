"use client";

import { useState } from "react";
import { EvaluationForm } from "@/components/EvaluationForm";
import { ResultsPanel } from "@/components/ResultsPanel";
import { ListingsExplorer } from "@/components/ListingsExplorer";
import type { EvaluationResponse } from "@/lib/types";

export default function Home() {
  const [result, setResult] = useState<EvaluationResponse | null>(null);

  return (
    <main className="app-shell">
      <header className="hero">
        <h1>AcquistoCase</h1>
        <p>
          Valuta se una casa è giusta per il tuo obiettivo e confronta gli annunci
          aggregati da più portali — punteggio, prezzo di mercato, servizi e mappa,
          tutto in un&apos;unica piattaforma.
        </p>
      </header>

      <div className="grid" style={{ marginTop: "1.5rem" }}>
        <section className="glass">
          <div className="section-title">Valuta un immobile</div>
          <EvaluationForm onResult={setResult} />
        </section>
        {result && (
          <section className="glass">
            <div className="section-title">Risultato</div>
            <ResultsPanel result={result} />
          </section>
        )}
      </div>

      <div style={{ marginTop: "1.5rem" }}>
        <ListingsExplorer />
      </div>
    </main>
  );
}
