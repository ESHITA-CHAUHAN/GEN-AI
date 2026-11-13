export function getAIConfig(env = process.env) {
  const hasNetlifyGateway = Boolean(env.NETLIFY_AI_GATEWAY_KEY && env.NETLIFY_AI_GATEWAY_URL);
  const apiKey = (hasNetlifyGateway ? env.NETLIFY_AI_GATEWAY_KEY : env.OPENAI_API_KEY) || "";
  const baseUrl = (hasNetlifyGateway ? env.NETLIFY_AI_GATEWAY_URL : env.OPENAI_BASE_URL || "").replace(/\/+$/, "");

  return {
    apiKey,
    baseUrl,
    ready: Boolean(apiKey && baseUrl),
    model: env.OPENAI_MODEL || "gpt-4o-mini",
  };
}

export function getChatCompletionsUrl(baseUrl) {
  const gatewayRoot = baseUrl.replace(/\/v1$/i, "");
  return `${gatewayRoot}/v1/chat/completions`;
}
