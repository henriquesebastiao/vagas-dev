// Todas as funções que conversam com sua FastAPI ficam aqui.
// Assim, se a URL da API mudar, você só muda neste arquivo.

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Busca vagas com filtros opcionais.
 * Qualquer filtro não preenchido é ignorado.
 */
export async function fetchJobs(filters = {}) {
  const params = new URLSearchParams();

  if (filters.keyword) params.set("keyword", filters.keyword);
  if (filters.level) params.set("level", filters.level);
  if (filters.workplace_type)
    params.set("workplace_type", filters.workplace_type);
  if (filters.location) params.set("location", filters.location);
  if (filters.source) params.set("source", filters.source);

  params.set("limit", filters.limit || 50);
  params.set("offset", filters.offset || 0);

  const res = await fetch(`${BASE_URL}/jobs?${params}`);
  if (!res.ok) throw new Error("Erro ao buscar vagas");
  return res.json();
}

/**
 * Busca as fontes disponíveis e a contagem de vagas de cada uma.
 * Usado para exibir os stats no header.
 */
export async function fetchSources() {
  const res = await fetch(`${BASE_URL}/jobs/sources`);
  if (!res.ok) throw new Error("Erro ao buscar fontes");
  return res.json();
}

/**
 * Dispara uma sincronização manual de uma fonte.
 * A FastAPI roda o sync em background e retorna imediatamente.
 */
export async function triggerSync(source = "gupy") {
  const res = await fetch(`${BASE_URL}/jobs/sync/${source}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Erro ao disparar sync");
  return res.json();
}
