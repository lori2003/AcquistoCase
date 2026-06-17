import "./globals.css";
import "leaflet/dist/leaflet.css";

export const metadata = {
  title: "AcquistoCase",
  description: "Valuta se una casa è giusta per il tuo obiettivo",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="it">
      <body>{children}</body>
    </html>
  );
}
