import type { Listing } from "@/lib/types";
import { formatEuro } from "@/lib/format";

export function ListingCard({ listing }: { listing: Listing }) {
  return (
    <article className="glass listing-card">
      {listing.image_url && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={listing.image_url} alt={listing.title ?? "Immobile"} />
      )}
      <span className="price">{formatEuro(listing.price_eur)}</span>
      <span className="meta">
        {listing.mq} m² · {formatEuro(listing.price_per_mq)}/m²
        {listing.rooms ? ` · ${listing.rooms} locali` : ""}
      </span>
      {listing.title && <strong>{listing.title}</strong>}
      {listing.address && <span className="meta">{listing.address}</span>}

      <div className="badges" aria-label="Portali di provenienza">
        {listing.sources.map((s) => (
          <span key={s} className="badge">
            {s}
          </span>
        ))}
      </div>

      {listing.url && (
        <a href={listing.url} target="_blank" rel="noreferrer">
          Vedi annuncio →
        </a>
      )}
    </article>
  );
}
