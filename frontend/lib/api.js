import { PAGE_SIZE, getApiUrl } from "@/lib/constants";

// Sem resposta nesse tempo, a API é tratada como indisponível.
const TIMEOUT_MS = 15000;

/**
 * Faz uma requisição à API e devolve o JSON. Qualquer falha (rede, timeout
 * ou status diferente de 2xx) vira exceção; a interface trata todas como
 * "API em manutenção".
 */
async function request(path, options = {}) {
  const res = await fetch(`${getApiUrl()}${path}`, {
    ...options,
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`API respondeu ${res.status}`);
  return res.json();
}

/**
 * Busca vagas com filtros opcionais.
 * Qualquer filtro não preenchido é ignorado.
 */
export function fetchJobs(filters = {}, offset = 0) {
  const params = new URLSearchParams();

  for (const key of [
    "keyword",
    "level",
    "workplace_type",
    "source",
    "company",
    "location",
  ]) {
    const value = filters[key]?.trim?.() ?? filters[key];
    if (value) params.set(key, value);
  }
  if (filters.for_pcd) params.set("for_pcd", "true");

  params.set("limit", PAGE_SIZE);
  params.set("offset", offset);

  return request(`/jobs?${params}`);
}

/** Busca as fontes disponíveis e a contagem de vagas de cada uma. */
export function fetchSources() {
  return request("/jobs/sources");
}

/** Verifica se a API voltou a responder. */
export function checkHealth() {
  return request("/health");
}

/**
 * Dispara uma sincronização manual de uma fonte.
 * A API roda o sync em background e responde imediatamente.
 */
export function triggerSync(source = "gupy") {
  return request(`/jobs/sync/${source}`, { method: "POST" });
}
