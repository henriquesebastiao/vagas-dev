"use client";
// Página principal — orquestra todos os componentes e gerencia o estado global.

import { useState, useEffect, useCallback } from "react";
import { fetchJobs, fetchSources, triggerSync } from "@/lib/api";
import Header from "@/components/Header";
import Filters from "@/components/Filters";
import JobCard from "@/components/JobCard";
import JobDetail from "@/components/JobDetail";

export default function Home() {
  const [jobs, setJobs] = useState([]);
  const [sources, setSources] = useState([]);
  const [selected, setSelected] = useState(null);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
  }, []);

  // Carrega as fontes uma vez ao abrir a página
  useEffect(() => {
    fetchSources()
      .then(setSources)
      .catch(() => setSources([]));
  }, []);

  // Recarrega as vagas sempre que os filtros mudam
  useEffect(() => {
    let cancelled = false;

    fetchJobs(filters)
      .then((data) => {
        if (cancelled) return;
        setJobs(data);
        setLoading(false);
        setError(null);
        setSelected((prev) =>
          prev && data.find((j) => j.id === prev.id) ? prev : null,
        );
      })
      .catch(() => {
        if (cancelled) return;
        setError(
          "Não foi possível carregar as vagas. Verifique se a API está rodando.",
        );
        setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [filters]);

  async function handleSync() {
    await triggerSync("gupy");
    fetchJobs(filters).then(setJobs);
  }

  return (
    <div
      style={{
        fontFamily: "'DM Sans', 'Segoe UI', sans-serif",
        background: "#0a0d14",
        minHeight: "100vh",
        color: "#f1f5f9",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Header sources={sources} />

      <div
        style={{
          display: "flex",
          flex: 1,
          overflow: "hidden",
        }}
      >
        {/* Painel esquerdo — filtros + lista de vagas */}
        <div
          style={{
            width: 450,
            minWidth: 450,
            borderRight: "1px solid rgba(255,255,255,0.07)",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            height: "calc(100vh - 105px)",
          }}
        >
          <Filters
            onChange={handleFilterChange}
            onSync={handleSync}
            totalJobs={jobs.length}
            sources={sources}
          />

          {/* Lista de vagas com scroll */}
          <div style={{ flex: 1, overflowY: "auto", padding: "8px 20px 20px" }}>
            {loading && (
              <div
                style={{
                  textAlign: "center",
                  color: "#475569",
                  marginTop: 48,
                  fontSize: 14,
                }}
              >
                Carregando vagas...
              </div>
            )}

            {error && !loading && (
              <div
                style={{
                  margin: "20px 0",
                  padding: 16,
                  background: "rgba(239,68,68,0.08)",
                  border: "1px solid rgba(239,68,68,0.2)",
                  borderRadius: 12,
                  color: "#f87171",
                  fontSize: 13,
                }}
              >
                {error}
              </div>
            )}

            {!loading && !error && jobs.length === 0 && (
              <div
                style={{
                  textAlign: "center",
                  color: "#475569",
                  marginTop: 60,
                  fontSize: 14,
                }}
              >
                Nenhuma vaga encontrada para esses filtros.
              </div>
            )}

            {!loading &&
              jobs.map((job) => (
                <JobCard
                  key={job.id}
                  job={job}
                  selected={selected?.id === job.id}
                  onClick={setSelected}
                />
              ))}
          </div>
        </div>

        {/* Painel direito — detalhes ou boas-vindas */}
        <div style={{ height: "calc(100vh - 105px)", overflowY: "auto" }}>
          <JobDetail job={selected} />
        </div>
      </div>

      <style>{`
        * { scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.1) transparent; }
        select option { background: #1e293b; }
      `}</style>
    </div>
  );
}
