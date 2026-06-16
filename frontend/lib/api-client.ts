import type { EvaluationRequest, EvaluationResponse } from "./types";

const DEFAULT_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function evaluate(
  request: EvaluationRequest,
  baseUrl: string = DEFAULT_BASE_URL,
): Promise<EvaluationResponse> {
  const res = await fetch(`${baseUrl}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) {
    throw new Error(`Errore dalla API: ${res.status}`);
  }
  return (await res.json()) as EvaluationResponse;
}
