import { API_URL, PAGE_SIZE } from "@/lib/constants";

/**
 * Busca vagas com filtros opcionais.
 * Qualquer filtro não preenchido é ignorado.
 */
export async function fetchJobs(filters = {}, offset = 0) {
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

  const res = await fetch(`${API_URL}/jobs?${params}`);
  if (!res.ok) throw new Error("Erro ao buscar vagas");
  return res.json();
}

/** Busca as fontes disponíveis e a contagem de vagas de cada uma. */
export async function fetchSources() {
  const res = await fetch(`${API_URL}/jobs/sources`);
  if (!res.ok) throw new Error("Erro ao buscar fontes");
  return res.json();
}

/**
 * Dispara uma sincronização manual de uma fonte.
 * A API roda o sync em background e responde imediatamente.
 */
export async function triggerSync(source = "gupy") {
  const res = await fetch(`${API_URL}/jobs/sync/${source}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Erro ao disparar sync");
  return res.json();
}
