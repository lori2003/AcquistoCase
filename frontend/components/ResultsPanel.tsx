import type { EvaluationResponse } from "@/lib/types";
import { formatDelta, formatMinutes } from "@/lib/format";
import { ScoreGauge } from "./ScoreGauge";
import { DataRisksNotice } from "./DataRisksNotice";

export function ResultsPanel({ result }: { result: EvaluationResponse }) {
  const { components, price_context } = result;
  return (
    <div aria-label="Risultato valutazione">
      <ScoreGauge score={result.final_score} />

      <p>
        {result.coherent_with_objective
          ? "Coerente con il tuo obiettivo"
          : "Non del tutto in linea con il tuo obiettivo"}
      </p>

      <ul>
        <li>Prezzo: {components.price_score}/100</li>
        <li>Distanza trasporti: {components.distance_score}/100</li>
        <li>Servizi: {components.services_score}/100</li>
        <li>Obiettivo: {components.objective_score}/100</li>
      </ul>

      <p>Prezzo vs mercato: {formatDelta(price_context.delta_pct_vs_market)}</p>

      <h3>Servizi più vicini</h3>
      <ul>
        {result.nearest_amenities.map((a) => (
          <li key={a.category}>
            {a.category}: {formatMinutes(a.walk_minutes)}
          </li>
        ))}
      </ul>

      <h3>Valutazione</h3>
      <p>{result.report_text}</p>

      <DataRisksNotice risks={result.data_risks} />

      {result.suggestions.length > 0 && (
        <section aria-label="Suggerimenti">
          <h3>Prossimi passi</h3>
          <ul>
            {result.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
