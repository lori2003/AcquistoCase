"use client";

import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";
import type { Listing } from "@/lib/types";
import { formatEuro } from "@/lib/format";

const DEFAULT_CENTER: [number, number] = [45.4642, 9.19]; // Milano

function center(listings: Listing[]): [number, number] {
  const pts = listings.filter((l) => l.lat != null && l.lon != null);
  if (pts.length === 0) return DEFAULT_CENTER;
  const lat = pts.reduce((s, l) => s + (l.lat as number), 0) / pts.length;
  const lon = pts.reduce((s, l) => s + (l.lon as number), 0) / pts.length;
  return [lat, lon];
}

export default function ListingsMap({ listings }: { listings: Listing[] }) {
  return (
    <div className="map-wrap">
      <MapContainer center={center(listings)} zoom={13} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {listings
          .filter((l) => l.lat != null && l.lon != null)
          .map((l) => (
            <CircleMarker
              key={l.id}
              center={[l.lat as number, l.lon as number]}
              radius={10}
              pathOptions={{ color: "#22e3ff", fillColor: "#22e3ff", fillOpacity: 0.6 }}
            >
              <Popup>
                <strong>{formatEuro(l.price_eur)}</strong>
                <br />
                {l.mq} m² · {l.sources.join(", ")}
              </Popup>
            </CircleMarker>
          ))}
      </MapContainer>
    </div>
  );
}
