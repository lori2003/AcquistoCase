import { expect, test } from "@playwright/test";

// Percorso felice: compila il form, invia, vede il punteggio.
// La chiamata alla API backend viene intercettata e mockata, così l'e2e
// resta deterministico e non richiede il backend in esecuzione.
test("compila il form e mostra il punteggio", async ({ page }) => {
  await page.route("**/api/evaluate", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        final_score: 75,
        components: { price_score: 80, distance_score: 70, services_score: 60, objective_score: 90 },
        coherent_with_objective: true,
        price_context: { price_per_mq: 2500, omi_min_per_mq: 2000, omi_max_per_mq: 3000, delta_pct_vs_market: 0, data_available: true },
        nearest_amenities: [],
        report_text: "Buon immobile.",
        data_risks: [],
        suggestions: [],
      }),
    });
  });

  await page.goto("/");
  await page.getByLabel("Città").fill("Milano");
  await page.getByLabel("Indirizzo").fill("Via Roma 1");
  await page.getByLabel("Budget (€)").fill("300000");
  await page.getByLabel("Prezzo (€)").fill("250000");
  await page.getByLabel("Metri quadri").fill("80");
  await page.getByRole("button", { name: /valuta immobile/i }).click();

  await expect(page.getByRole("meter")).toHaveAttribute("aria-valuenow", "75");
});
