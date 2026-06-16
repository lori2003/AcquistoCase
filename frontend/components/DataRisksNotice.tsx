import type { DataRisk } from "@/lib/types";

export function DataRisksNotice({ risks }: { risks: DataRisk[] }) {
  if (risks.length === 0) return null;
  return (
    <section aria-label="Rischi dei dati">
      <h3>Limiti e rischi dei dati</h3>
      <ul>
        {risks.map((r) => (
          <li key={r.code}>{r.message}</li>
        ))}
      </ul>
    </section>
  );
}
