// Rótulos e formatadores compartilhados entre componentes.

export const LEVEL_LABELS = {
  estagio: "Estágio",
  trainee: "Trainee",
  junior: "Júnior",
  pleno: "Pleno",
  senior: "Sênior",
};

export const WORKPLACE_LABELS = {
  remote: "Remoto",
  hybrid: "Híbrido",
  "on-site": "Presencial",
};

export const SOURCE_LABELS = {
  gupy: "Gupy",
  linkedin: "LinkedIn",
};

export const PAGE_SIZE = 50;

const BUILD_API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * URL da API. Prioriza o valor de execução definido em /config.js (gerado
 * pelo container Docker) e cai para o valor embutido no build.
 */
export function getApiUrl() {
  if (typeof window !== "undefined" && window.__VAGAS_CONFIG__?.apiUrl) {
    return window.__VAGAS_CONFIG__.apiUrl;
  }
  return BUILD_API_URL;
}

/** Transforma uma data ISO em tempo relativo curto ("há 3 h"). */
export function timeAgo(dateStr) {
  const date = new Date(dateStr);
  if (Number.isNaN(date.getTime())) return "";
  const minutes = Math.max(0, Math.floor((Date.now() - date) / 60000));
  if (minutes < 1) return "agora";
  if (minutes < 60) return `há ${minutes} min`;
  if (minutes < 1440) return `há ${Math.floor(minutes / 60)} h`;
  return `há ${Math.floor(minutes / 1440)} d`;
}

const dateFormat = new Intl.DateTimeFormat("pt-BR", {
  day: "2-digit",
  month: "short",
  year: "numeric",
});

/** Formata uma data ISO como "12 de mar. de 2026"; null vira "—". */
export function formatDate(dateStr) {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  return Number.isNaN(date.getTime()) ? "—" : dateFormat.format(date);
}

export function formatNumber(n) {
  return Number(n || 0).toLocaleString("pt-BR");
}

/** Extrai o domínio de uma URL para mostrar onde a candidatura acontece. */
export function hostOf(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "";
  }
}
