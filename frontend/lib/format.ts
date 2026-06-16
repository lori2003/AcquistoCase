// Helper di formattazione puri (facilmente testabili al 100%).

export type ScoreColor = "red" | "orange" | "green";

export function scoreColor(score: number): ScoreColor {
  if (score < 50) return "red";
  if (score < 80) return "orange";
  return "green";
}

export function formatEuro(value: number): string {
  return new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatMinutes(minutes: number | null): string {
  if (minutes === null || minutes === undefined) return "n/d";
  return `${Math.round(minutes)} min a piedi`;
}

export function formatDelta(deltaPct: number | null): string {
  if (deltaPct === null || deltaPct === undefined) return "dato non disponibile";
  const sign = deltaPct > 0 ? "+" : "";
  const verso = deltaPct < 0 ? "sotto" : deltaPct > 0 ? "sopra" : "in linea con il";
  return `${sign}${deltaPct}% (${verso} mercato)`;
}
