import { useSyncExternalStore } from "react";
import { getApiUrl } from "@/lib/constants";

const BUILD_API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// A configuração vem de /config.js e não muda depois de carregada.
const subscribe = () => () => {};

/**
 * Versão em hook de getApiUrl() para links renderizados. No HTML
 * pré-renderizado usa o valor do build; no navegador, o de execução,
 * sem causar erro de hidratação.
 */
export function useApiUrl() {
  return useSyncExternalStore(subscribe, getApiUrl, () => BUILD_API_URL);
}
