interface Env {
  AI: Ai;
  ROUTING_PRIORITY: string;
  SPENDING_POLICY: string;
  AUTOMATIC_FALLBACK: string;
  MATRIX_GATEWAY_TOKEN?: string;
}
type Model = { id: string; provider: "workers-ai"; modalities: string[]; freeVerified: boolean; qualityScore?: number };
const registry: Model[] = []; // Fail closed: populate only after verified model/free quota inventory.
function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
}
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/health" && request.method === "GET") return json({ status: "ready-for-configuration", inferenceEnabled: false });
    const expected = env.MATRIX_GATEWAY_TOKEN;
    const authorization = request.headers.get("authorization");
    if (!expected || authorization !== `Bearer ${expected}`) return json({ error: "UNAUTHORIZED" }, 401);
    if (url.pathname === "/v1/models" && request.method === "GET") return json({ models: registry });
    if (url.pathname === "/v1/route" && request.method === "POST") {
      if (env.SPENDING_POLICY !== "free") return json({ error: "POLICY_INVALID" }, 503);
      return json({ error: "FREE_CAPACITY_UNAVAILABLE", reason: "No verified free models configured; inference disabled until certification" }, 503);
    }
    return json({ error: "NOT_FOUND" }, 404);
  }
} satisfies ExportedHandler<Env>;
