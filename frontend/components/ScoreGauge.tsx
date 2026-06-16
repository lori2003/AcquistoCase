import { scoreColor } from "@/lib/format";

const COLORS: Record<string, string> = {
  red: "#c0392b",
  orange: "#e67e22",
  green: "#27ae60",
};

export function ScoreGauge({ score }: { score: number }) {
  const color = scoreColor(score);
  return (
    <div role="meter" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}>
      <span style={{ color: COLORS[color], fontSize: "2rem", fontWeight: 700 }}>
        {score}
      </span>
      <span>/100</span>
    </div>
  );
}
