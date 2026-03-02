// Barra de busca e filtros do painel esquerdo.
// Usa debounce na busca por keyword para não disparar um request a cada tecla.

import { useState, useEffect } from "react";
import { LEVEL_CONFIG, WORKPLACE_CONFIG } from "@/lib/constants";

// Aguarda o usuário parar de digitar por `delay` ms antes de chamar a função.
// Evita uma requisição para cada letra digitada.
function useDebounce(value, delay = 400) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer); // cancela o timer se o valor mudar antes do delay
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
          minWidth: 130,
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

export default function Filters({ onChange, onSync, totalJobs }) {
  const [keyword, setKeyword] = useState("");
  const [level, setLevel] = useState("");
  const [workplaceType, setWorkplaceType] = useState("");
  const [syncing, setSyncing] = useState(false);

  // Aplica debounce na keyword para não buscar a cada tecla
  const debouncedKeyword = useDebounce(keyword);

  // Sempre que qualquer filtro mudar, avisa o componente pai (page.js)
  useEffect(() => {
    onChange({
      keyword: debouncedKeyword,
      level,
      workplace_type: workplaceType,
    });
  }, [debouncedKeyword, level, workplaceType, onChange]);

  async function handleSync() {
    setSyncing(true);
    try {
      await onSync();
    } finally {
      setTimeout(() => setSyncing(false), 2000);
    }
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

      {/* Campo de busca */}
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
            placeholder="Buscar por título, empresa..."
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

      {/* Filtros de select */}
      <div
        style={{
          padding: "12px 20px 16px",
          display: "flex",
          gap: 12,
          flexWrap: "wrap",
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
    </div>
  );
}
