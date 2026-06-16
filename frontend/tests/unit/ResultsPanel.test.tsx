import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ResultsPanel } from "@/components/ResultsPanel";
import type { EvaluationResponse } from "@/lib/types";

function makeResult(overrides: Partial<EvaluationResponse> = {}): EvaluationResponse {
  return {
    final_score: 82,
    components: {
      price_score: 90,
      distance_score: 80,
      services_score: 70,
      objective_score: 85,
    },
    coherent_with_objective: true,
    price_context: {
      price_per_mq: 2500,
      omi_min_per_mq: 2000,
      omi_max_per_mq: 3000,
      delta_pct_vs_market: 0,
      data_available: true,
    },
    nearest_amenities: [
      { category: "metro", name: "M1", walk_minutes: 5, distance_m: 400 },
    ],
    report_text: "Ottimo immobile.",
    data_risks: [],
    suggestions: ["Verifica le spese condominiali."],
    ...overrides,
  };
}

describe("ResultsPanel", () => {
  it("renders final score and the four components", () => {
    render(<ResultsPanel result={makeResult()} />);
    expect(screen.getByRole("meter")).toHaveAttribute("aria-valuenow", "82");
    expect(screen.getByText(/Prezzo: 90\/100/)).toBeInTheDocument();
    expect(screen.getByText(/Distanza trasporti: 80\/100/)).toBeInTheDocument();
    expect(screen.getByText(/Servizi: 70\/100/)).toBeInTheDocument();
    expect(screen.getByText(/Obiettivo: 85\/100/)).toBeInTheDocument();
  });

  it("renders the data risks notice when risks are present", () => {
    const result = makeResult({
      data_risks: [{ code: "AI_UNAVAILABLE", message: "Report AI non disponibile." }],
      report_text: "Sintesi locale.",
    });
    render(<ResultsPanel result={result} />);
    expect(screen.getByRole("region", { name: /rischi dei dati/i })).toBeInTheDocument();
    expect(screen.getByText("Report AI non disponibile.")).toBeInTheDocument();
    expect(screen.getByText("Sintesi locale.")).toBeInTheDocument();
  });

  it("hides the data risks notice when there are none", () => {
    render(<ResultsPanel result={makeResult()} />);
    expect(screen.queryByRole("region", { name: /rischi dei dati/i })).not.toBeInTheDocument();
  });
});
