"use client";

import { useState, type ComponentType } from "react";
import dynamic from "next/dynamic";
import { fetchListings } from "@/lib/api-client";
import type { Listing } from "@/lib/types";
import { ListingCard } from "./ListingCard";

// La mappa Leaflet va caricata solo lato client (usa `window`).
const DynamicMap = dynamic(() => import("./ListingsMap"), { ssr: false });

export function ListingsExplorer({
  MapComponent = DynamicMap,
}: {
  MapComponent?: ComponentType<{ listings: Listing[] }>;
}) {
  const [city, setCity] = useState("Milano");
  const [listings, setListings] = useState<Listing[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      setListings(await fetchListings(city));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="glass">
      <div className="section-title">Annunci aggregati</div>
      <form onSubmit={handleSearch} aria-label="Cerca annunci">
        <label>
          Città
          <input value={city} onChange={(e) => setCity(e.target.value)} />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Cerco…" : "Cerca annunci"}
        </button>
      </form>

      {error && <p role="alert">{error}</p>}

      {listings && (
        <>
          <p className="meta">
            {listings.length} immobili trovati e deduplicati da più portali
          </p>
          <div style={{ margin: "1rem 0" }}>
            <MapComponent listings={listings} />
          </div>
          <div className="grid">
            {listings.map((l) => (
              <ListingCard key={l.id} listing={l} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
