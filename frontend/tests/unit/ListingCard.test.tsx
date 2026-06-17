import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ListingCard } from "@/components/ListingCard";
import type { Listing } from "@/lib/types";

function makeListing(overrides: Partial<Listing> = {}): Listing {
  return {
    id: "abc",
    title: "Trilocale Navigli",
    price_eur: 250000,
    mq: 80,
    price_per_mq: 3125,
    rooms: 3,
    address: "Via Vigevano 12",
    city: "Milano",
    lat: 45.46,
    lon: 9.17,
    url: "https://example.com/1",
    image_url: null,
    sources: ["immobiliare", "idealista"],
    ...overrides,
  };
}

describe("ListingCard", () => {
  it("shows price, size and price per mq", () => {
    render(<ListingCard listing={makeListing()} />);
    expect(screen.getByText(/250\.000/)).toBeInTheDocument();
    expect(screen.getByText(/80 m²/)).toBeInTheDocument();
  });

  it("renders one badge per source portal", () => {
    render(<ListingCard listing={makeListing()} />);
    const badges = screen.getByLabelText(/portali di provenienza/i);
    expect(badges).toHaveTextContent("immobiliare");
    expect(badges).toHaveTextContent("idealista");
  });

  it("links to the original listing", () => {
    render(<ListingCard listing={makeListing()} />);
    expect(screen.getByRole("link", { name: /vedi annuncio/i })).toHaveAttribute(
      "href",
      "https://example.com/1",
    );
  });
});
