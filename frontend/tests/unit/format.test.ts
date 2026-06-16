import { describe, expect, it } from "vitest";
import {
  formatDelta,
  formatEuro,
  formatMinutes,
  scoreColor,
} from "@/lib/format";

describe("scoreColor", () => {
  it.each([
    [0, "red"],
    [49, "red"],
    [50, "orange"],
    [79, "orange"],
    [80, "green"],
    [100, "green"],
  ])("score %i -> %s", (score, expected) => {
    expect(scoreColor(score as number)).toBe(expected);
  });
});

describe("formatEuro", () => {
  it("formats with euro symbol and no decimals", () => {
    const out = formatEuro(250000);
    expect(out).toContain("250.000");
    expect(out).toContain("€");
  });
});

describe("formatMinutes", () => {
  it("returns n/d for null", () => {
    expect(formatMinutes(null)).toBe("n/d");
  });
  it("rounds minutes", () => {
    expect(formatMinutes(5.4)).toBe("5 min a piedi");
  });
});

describe("formatDelta", () => {
  it("handles missing data", () => {
    expect(formatDelta(null)).toBe("dato non disponibile");
  });
  it("marks below market for negative delta", () => {
    expect(formatDelta(-12)).toContain("sotto");
  });
  it("marks above market for positive delta", () => {
    expect(formatDelta(8)).toContain("sopra");
    expect(formatDelta(8)).toContain("+8%");
  });
});
