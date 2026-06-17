import { beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ListingsExplorer } from "@/components/ListingsExplorer";
import type { Listing } from "@/lib/types";

const fetchListingsMock = vi.fn();
vi.mock("@/lib/api-client", () => ({
  fetchListings: (...args: unknown[]) => fetchListingsMock(...args),
}));

// Stub della mappa, così il test non carica Leaflet.
function StubMap({ listings }: { listings: Listing[] }) {
  return <div data-testid="map-stub">mappa: {listings.length}</div>;
}

const sample: Listing[] = [
  {
    id: "1",
    title: "Trilocale",
    price_eur: 250000,
    mq: 80,
    price_per_mq: 3125,
    rooms: 3,
    address: "Via Vigevano 12",
    city: "Milano",
    lat: 45.46,
    lon: 9.17,
    url: null,
    image_url: null,
    sources: ["immobiliare", "idealista"],
  },
];

beforeEach(() => {
  fetchListingsMock.mockReset();
});

describe("ListingsExplorer", () => {
  it("fetches listings and renders cards plus the map", async () => {
    const user = userEvent.setup();
    fetchListingsMock.mockResolvedValue(sample);
    render(<ListingsExplorer MapComponent={StubMap} />);

    await user.click(screen.getByRole("button", { name: /cerca annunci/i }));

    expect(fetchListingsMock).toHaveBeenCalledWith("Milano");
    expect(await screen.findByText(/1 immobili trovati/i)).toBeInTheDocument();
    expect(screen.getByTestId("map-stub")).toHaveTextContent("mappa: 1");
    expect(screen.getByLabelText(/portali di provenienza/i)).toBeInTheDocument();
  });

  it("shows an error when the API fails", async () => {
    const user = userEvent.setup();
    fetchListingsMock.mockRejectedValue(new Error("Errore dalla API: 500"));
    render(<ListingsExplorer MapComponent={StubMap} />);

    await user.click(screen.getByRole("button", { name: /cerca annunci/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/500/);
  });
});
