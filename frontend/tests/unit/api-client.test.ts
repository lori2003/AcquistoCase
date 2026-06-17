import { afterEach, describe, expect, it, vi } from "vitest";
import { evaluate, fetchListings } from "@/lib/api-client";
import type { EvaluationRequest } from "@/lib/types";

const request: EvaluationRequest = {
  property: { city: "Milano", address: "Via Roma 1", budget_eur: 300000, price_eur: 250000, mq: 80 },
  objective: "near_metro",
  preferences: { metro: 1 },
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("evaluate", () => {
  it("POSTs to /api/evaluate and returns the parsed body", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ final_score: 88 }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await evaluate(request, "http://api.test");

    expect(fetchMock).toHaveBeenCalledWith(
      "http://api.test/api/evaluate",
      expect.objectContaining({ method: "POST" }),
    );
    expect(result).toEqual({ final_score: 88 });
  });

  it("throws on a non-ok response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500 }));
    await expect(evaluate(request, "http://api.test")).rejects.toThrow(/500/);
  });
});

describe("fetchListings", () => {
  it("GETs /api/listings with the city query and returns the array", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [{ id: "1" }],
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchListings("Milano", "http://api.test");

    expect(fetchMock).toHaveBeenCalledWith("http://api.test/api/listings?city=Milano");
    expect(result).toEqual([{ id: "1" }]);
  });

  it("throws on a non-ok response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 404 }));
    await expect(fetchListings("Milano", "http://api.test")).rejects.toThrow(/404/);
  });
});
