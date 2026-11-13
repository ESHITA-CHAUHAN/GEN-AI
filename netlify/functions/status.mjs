import { getAIConfig } from "./ai-config.mjs";

const json = (value) => new Response(JSON.stringify(value), {
  status: 200,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "http://localhost:8888",
    "Vary": "Origin",
  },
});

export default async function status(request) {
  if (request.method !== "GET") {
    return new Response("Method not allowed", {
      status: 405,
      headers: { Allow: "GET", "Cache-Control": "no-store" },
    });
  }

  const { ready, model } = getAIConfig();
  return json({
    ready,
    model: ready ? model : null,
  });
}

export const config = {
  path: "/api/status",
  method: ["GET"],
};
