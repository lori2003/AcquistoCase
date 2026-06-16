"use client";

import { useState } from "react";
import { EvaluationForm } from "@/components/EvaluationForm";
import { ResultsPanel } from "@/components/ResultsPanel";
import type { EvaluationResponse } from "@/lib/types";

export default function Home() {
  const [result, setResult] = useState<EvaluationResponse | null>(null);

  return (
    <main style={{ maxWidth: 640, margin: "0 auto", padding: "1rem" }}>
      <h1>AcquistoCase</h1>
      <p>Inserisci i dati dell&apos;immobile e il tuo obiettivo per ottenere un punteggio da 0 a 100.</p>
      <EvaluationForm onResult={setResult} />
      {result && <ResultsPanel result={result} />}
    </main>
  );
}
