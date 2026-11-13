"use client";
// Página principal: guarda o estado dos filtros, da lista e da vaga aberta.

import { useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import { checkHealth, fetchJobs, fetchSources, triggerSync } from "@/lib/api";
import { PAGE_SIZE, formatNumber } from "@/lib/constants";
import Header from "@/components/Header";
import Filters from "@/components/Filters";
import JobCard from "@/components/JobCard";
import JobDetail from "@/components/JobDetail";
import Maintenance from "@/components/Maintenance";

// Intervalo entre as verificações de volta da API durante a manutenção.
const HEALTH_POLL_MS = 20000;

export default function Home() {
  const [jobs, setJobs] = useState([]);
  const [sources, setSources] = useState([]);
  const [selected, setSelected] = useState(null);
  const [filters, setFilters] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [maintenance, setMaintenance] = useState(false);
  const [notice, setNotice] = useState(null);
  const [syncing, setSyncing] = useState(false);

  const handleFilterChange = useCallback((next) => setFilters(next), []);

  // Recarrega as fontes ao abrir a página e sempre que a API volta.
  useEffect(() => {
    if (maintenance) return;
    fetchSources()
      .then(setSources)
      .catch(() => {
        setSources([]);
        setMaintenance(true);
      });
  }, [maintenance]);

  // Em manutenção, verifica periodicamente se a API voltou. Ao sair da
  // manutenção os filtros são remontados e recarregam a lista.
  useEffect(() => {
    if (!maintenance) return;
    const check = () =>
      checkHealth()
        .then(() => setMaintenance(false))
        .catch(() => {});
    const timer = setInterval(check, HEALTH_POLL_MS);
    window.addEventListener("online", check);
    return () => {
      clearInterval(timer);
      window.removeEventListener("online", check);
    };
  }, [maintenance]);

  // Recarrega a primeira página sempre que os filtros mudam.
  useEffect(() => {
    if (!filters) return;
    let cancelled = false;
    setLoading(true);

    fetchJobs(filters)
      .then((data) => {
        if (cancelled) return;
        setJobs(data);
        setHasMore(data.length === PAGE_SIZE);
        setSelected((prev) =>
          prev && data.some((j) => j.id === prev.id) ? prev : null,
        );
      })
      .catch(() => !cancelled && setMaintenance(true))
      .finally(() => !cancelled && setLoading(false));

    return () => {
      cancelled = true;
    };
  }, [filters]);

  // Fecha o painel de leitura com Esc (útil no celular).
  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && setSelected(null);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  async function loadMore() {
    setLoadingMore(true);
    try {
      const data = await fetchJobs(filters, jobs.length);
      setJobs((prev) => [...prev, ...data]);
      setHasMore(data.length === PAGE_SIZE);
    } catch {
      setMaintenance(true);
    } finally {
      setLoadingMore(false);
    }
  }

  async function handleSync() {
    setSyncing(true);
    try {
      await triggerSync("gupy");
      setNotice(
        "Busca na Gupy iniciada. As vagas novas aparecem aqui em alguns minutos.",
      );
    } catch {
      setMaintenance(true);
    } finally {
      setSyncing(false);
    }
  }

  if (maintenance) {
    return (
      <div className="app app--maintenance">
        <Header sources={[]} />
        <Maintenance />
      </div>
    );
  }

  return (
    <div className="app">
      <Header sources={sources} />
      <Filters onChange={handleFilterChange} sources={sources} />

      <main className="workspace">
        <section className="list-pane" aria-label="Vagas">
          <div className="list-head">
            <span className="mono">
              {loading
                ? "Carregando…"
                : `${formatNumber(jobs.length)}${hasMore ? "+" : ""} vagas`}
            </span>
            <button
              type="button"
              className="link-button"
              onClick={handleSync}
              disabled={syncing}
            >
              <RefreshCw size={13} aria-hidden="true" />
              {syncing ? "Iniciando…" : "Buscar vagas novas"}
            </button>
          </div>

          <div className="list-body">
            {notice && <p className="list-notice">{notice}</p>}

            {!loading && jobs.length === 0 && (
              <div className="list-state">
                Nenhuma vaga com esses filtros. Tente remover algum deles.
              </div>
            )}

            {jobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                selected={selected?.id === job.id}
                onSelect={setSelected}
              />
            ))}

            {hasMore && !loading && (
              <button
                type="button"
                className="load-more"
                onClick={loadMore}
                disabled={loadingMore}
              >
                {loadingMore ? "Carregando…" : "Carregar mais vagas"}
              </button>
            )}
          </div>
        </section>

        <section
          className={`detail-pane${selected ? " is-open" : ""}`}
          aria-label="Detalhes da vaga"
        >
          <JobDetail
            key={selected?.id}
            job={selected}
            sources={sources}
            onBack={() => setSelected(null)}
          />
        </section>
      </main>
    </div>
  );
}
