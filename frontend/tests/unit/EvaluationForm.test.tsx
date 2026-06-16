import { beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { EvaluationForm } from "@/components/EvaluationForm";

const evaluateMock = vi.fn();
vi.mock("@/lib/api-client", () => ({
  evaluate: (...args: unknown[]) => evaluateMock(...args),
}));

beforeEach(() => {
  evaluateMock.mockReset();
});

describe("EvaluationForm", () => {
  it("blocks submit and shows error when required fields are empty", async () => {
    const user = userEvent.setup();
    render(<EvaluationForm onResult={vi.fn()} />);
    await user.click(screen.getByRole("button", { name: /valuta immobile/i }));
    expect(screen.getByRole("alert")).toHaveTextContent(/città e indirizzo/i);
    expect(evaluateMock).not.toHaveBeenCalled();
  });

  it("shows a validation error when mq is zero", async () => {
    const user = userEvent.setup();
    render(<EvaluationForm onResult={vi.fn()} />);
    await user.type(screen.getByLabelText("Città"), "Milano");
    await user.type(screen.getByLabelText("Indirizzo"), "Via Roma 1");
    await user.type(screen.getByLabelText("Budget (€)"), "300000");
    await user.type(screen.getByLabelText("Prezzo (€)"), "250000");
    await user.type(screen.getByLabelText("Metri quadri"), "0");
    await user.click(screen.getByRole("button", { name: /valuta immobile/i }));
    expect(screen.getByRole("alert")).toHaveTextContent(/metri quadri/i);
    expect(evaluateMock).not.toHaveBeenCalled();
  });

  it("renders all objective options", () => {
    render(<EvaluationForm onResult={vi.fn()} />);
    const select = screen.getByLabelText("Obiettivo") as HTMLSelectElement;
    expect(select.options).toHaveLength(6);
  });

  it("calls the api-client with the correct payload and forwards the result", async () => {
    const user = userEvent.setup();
    const onResult = vi.fn();
    evaluateMock.mockResolvedValue({ final_score: 70 });
    render(<EvaluationForm onResult={onResult} />);

    await user.type(screen.getByLabelText("Città"), "Milano");
    await user.type(screen.getByLabelText("Indirizzo"), "Via Roma 1");
    await user.type(screen.getByLabelText("Budget (€)"), "300000");
    await user.type(screen.getByLabelText("Prezzo (€)"), "250000");
    await user.type(screen.getByLabelText("Metri quadri"), "80");
    await user.click(screen.getByRole("button", { name: /valuta immobile/i }));

    expect(evaluateMock).toHaveBeenCalledTimes(1);
    const payload = evaluateMock.mock.calls[0][0];
    expect(payload.property).toMatchObject({
      city: "Milano",
      address: "Via Roma 1",
      budget_eur: 300000,
      price_eur: 250000,
      mq: 80,
    });
    expect(payload.objective).toBe("near_metro");
    expect(onResult).toHaveBeenCalledWith({ final_score: 70 });
  });
});
