// Barra de busca e filtros do painel esquerdo.
// Usa debounce na busca por keyword para não disparar um request a cada tecla.

import { useState, useEffect } from "react";
import { LEVEL_CONFIG, WORKPLACE_CONFIG } from "@/lib/constants";

function useDebounce(value, delay = 400) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

function FilterSelect({ label, value, onChange, options }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
      <label
        style={{
          fontSize: 11,
          fontWeight: 600,
          color: "#64748b",
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{
          background: "rgba(255,255,255,0.05)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: 9,
          padding: "8px 12px",
          color: value ? "#f1f5f9" : "#64748b",
          fontSize: 13,
          cursor: "pointer",
          outline: "none",
          appearance: "none",
          width: "100%",
        }}
      >
        <option value="">Todos</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );
}

function FilterInput({ label, placeholder, value, onChange }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
      <label
        style={{
          fontSize: 11,
          fontWeight: 600,
          color: "#64748b",
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        {label}
      </label>
      <input
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{
          width: "100%",
          boxSizing: "border-box",
          background: "rgba(255,255,255,0.05)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: 9,
          padding: "8px 12px",
          color: "#f1f5f9",
          fontSize: 13,
          outline: "none",
        }}
      />
    </div>
  );
}

function FilterToggle({ label, value, onChange }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 5,
        justifyContent: "flex-end",
      }}
    >
      <label
        style={{
          fontSize: 11,
          fontWeight: 600,
          color: "#64748b",
          letterSpacing: "0.06em",
          textTransform: "uppercase",
        }}
      >
        {label}
      </label>
      <button
        onClick={() => onChange(!value)}
        style={{
          background: value
            ? "rgba(251,191,36,0.15)"
            : "rgba(255,255,255,0.05)",
          border: value
            ? "1px solid rgba(251,191,36,0.4)"
            : "1px solid rgba(255,255,255,0.1)",
          borderRadius: 9,
          padding: "8px 12px",
          color: value ? "#fbbf24" : "#64748b",
          fontSize: 13,
          fontWeight: 600,
          cursor: "pointer",
          transition: "all 0.18s",
          textAlign: "left",
          whiteSpace: "nowrap",
        }}
      >
        ♿ {value ? "Somente PCD" : "Qualquer"}
      </button>
    </div>
  );
}

// Controla se os filtros avançados estão expandidos
export default function Filters({ onChange, onSync, totalJobs, sources = [] }) {
  const [keyword, setKeyword] = useState("");
  const [level, setLevel] = useState("");
  const [workplaceType, setWorkplaceType] = useState("");
  const [source, setSource] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [forPcd, setForPcd] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [syncing, setSyncing] = useState(false);

  const debouncedKeyword = useDebounce(keyword);
  const debouncedCompany = useDebounce(company);
  const debouncedLocation = useDebounce(location);

  const hasActiveFilters =
    level || workplaceType || source || company || location || forPcd;

  useEffect(() => {
    onChange({
      keyword: debouncedKeyword,
      level,
      workplace_type: workplaceType,
      source,
      company: debouncedCompany,
      location: debouncedLocation,
      for_pcd: forPcd || undefined,
    });
  }, [
    debouncedKeyword,
    level,
    workplaceType,
    source,
    debouncedCompany,
    debouncedLocation,
    forPcd,
    onChange,
  ]);

  async function handleSync() {
    setSyncing(true);
    try {
      await onSync();
    } finally {
      setTimeout(() => setSyncing(false), 2000);
    }
  }

  function clearFilters() {
    setKeyword("");
    setLevel("");
    setWorkplaceType("");
    setSource("");
    setCompany("");
    setLocation("");
    setForPcd(false);
  }

  return (
    <div style={{ borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
      {/* Header */}
      <div
        style={{
          padding: "16px 20px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          borderBottom: "1px solid rgba(255,255,255,0.05)",
        }}
      >
        <div style={{ fontSize: 13, color: "#64748b", fontWeight: 600 }}>
          {totalJobs ?? "–"} vagas encontradas
        </div>
        <button
          onClick={handleSync}
          style={{
            background: syncing
              ? "rgba(99,102,241,0.2)"
              : "rgba(99,102,241,0.12)",
            border: "1px solid rgba(99,102,241,0.3)",
            borderRadius: 8,
            color: "#818cf8",
            padding: "6px 13px",
            fontSize: 12,
            fontWeight: 600,
            cursor: "pointer",
            transition: "all 0.2s",
          }}
        >
          {syncing ? "⟳ Sincronizando..." : "⟳ Sync"}
        </button>
      </div>

      {/* Campo de busca principal */}
      <div
        style={{
          padding: "14px 20px 10px",
          borderBottom: "1px solid rgba(255,255,255,0.05)",
        }}
      >
        <div style={{ position: "relative" }}>
          <span
            style={{
              position: "absolute",
              left: 12,
              top: "50%",
              transform: "translateY(-50%)",
              fontSize: 14,
              color: "#475569",
            }}
          >
            🔍
          </span>
          <input
            placeholder="Buscar por título..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            style={{
              width: "100%",
              boxSizing: "border-box",
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: 10,
              padding: "10px 12px 10px 36px",
              color: "#f1f5f9",
              fontSize: 14,
              outline: "none",
            }}
          />
        </div>
      </div>

      {/* Filtros principais: Nível + Modalidade */}
      <div
        style={{
          padding: "12px 20px 0",
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 10,
        }}
      >
        <FilterSelect
          label="Nível"
          value={level}
          onChange={setLevel}
          options={Object.entries(LEVEL_CONFIG).map(([value, d]) => ({
            value,
            label: d.label,
          }))}
        />
        <FilterSelect
          label="Modalidade"
          value={workplaceType}
          onChange={setWorkplaceType}
          options={Object.entries(WORKPLACE_CONFIG).map(([value, d]) => ({
            value,
            label: d.label,
          }))}
        />
      </div>

      {/* Botão para expandir filtros avançados */}
      <div style={{ padding: "10px 20px 0" }}>
        <button
          onClick={() => setExpanded((v) => !v)}
          style={{
            background: "none",
            border: "none",
            color: hasActiveFilters ? "#818cf8" : "#475569",
            fontSize: 12,
            fontWeight: 600,
            cursor: "pointer",
            padding: "4px 0",
            display: "flex",
            alignItems: "center",
            gap: 5,
            letterSpacing: "0.03em",
          }}
        >
          <span
            style={{
              display: "inline-block",
              transition: "transform 0.2s",
              transform: expanded ? "rotate(180deg)" : "rotate(0deg)",
            }}
          >
            ▾
          </span>
          Filtros avançados
          {hasActiveFilters && (
            <span
              style={{
                background: "rgba(99,102,241,0.25)",
                color: "#818cf8",
                borderRadius: 10,
                padding: "1px 7px",
                fontSize: 10,
                fontWeight: 700,
              }}
            >
              ativos
            </span>
          )}
        </button>
      </div>

      {/* Painel de filtros avançados */}
      {expanded && (
        <div
          style={{
            padding: "12px 20px 16px",
            display: "flex",
            flexDirection: "column",
            gap: 10,
            borderTop: "1px solid rgba(255,255,255,0.04)",
            marginTop: 8,
          }}
        >
          {/* Fonte */}
          <FilterSelect
            label="Fonte"
            value={source}
            onChange={setSource}
            options={sources.map((s) => ({
              value: s.source,
              label: `${s.source} (${s.count})`,
            }))}
          />

          {/* Empresa */}
          <FilterInput
            label="Empresa"
            placeholder="Ex: Nubank, iFood..."
            value={company}
            onChange={setCompany}
          />

          {/* Localização */}
          <FilterInput
            label="Localização"
            placeholder="Ex: São Paulo, Remoto..."
            value={location}
            onChange={setLocation}
          />

          {/* PCD */}
          <FilterToggle
            label="Acessibilidade"
            value={forPcd}
            onChange={setForPcd}
          />

          {/* Limpar filtros */}
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              style={{
                background: "rgba(239,68,68,0.08)",
                border: "1px solid rgba(239,68,68,0.2)",
                borderRadius: 9,
                color: "#f87171",
                fontSize: 12,
                fontWeight: 600,
                padding: "8px 12px",
                cursor: "pointer",
                marginTop: 2,
              }}
            >
              ✕ Limpar filtros avançados
            </button>
          )}
        </div>
      )}

      {/* Espaçamento inferior */}
      <div style={{ height: expanded ? 0 : 14 }} />
    </div>
  );
}
