// Barra superior com logo, status da API e estatísticas gerais.

import { BriefcaseBusiness } from "lucide-react";

export default function Header({ sources }) {
  // Soma total de vagas de todas as fontes
  const totalJobs = sources.reduce((acc, s) => acc + s.count, 0);

  return (
    <header
      style={{
        padding: "0 32px",
        borderBottom: "1px solid rgba(255,255,255,0.07)",
        background: "rgba(255,255,255,0.015)",
        backdropFilter: "blur(12px)",
        position: "sticky",
        top: 0,
        zIndex: 10,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Linha superior: logo + status */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "16px 0",
          borderBottom: "1px solid rgba(255,255,255,0.05)",
        }}
      >
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              width: 34,
              height: 34,
              borderRadius: 10,
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 16,
              boxShadow: "0 0 20px rgba(99,102,241,0.35)",
            }}
          >
            <BriefcaseBusiness size={20} color="#fff" />
          </div>
          <div>
            <div
              style={{
                fontWeight: 800,
                fontSize: 17,
                letterSpacing: "-0.02em",
              }}
            >
              Vagas DEV
            </div>
            <div style={{ fontSize: 11, color: "#475569", marginTop: -1 }}>
              Agregador de vagas de emprego para desenvolvedores
            </div>
          </div>
        </div>

        {/* Status da API */}
        <div
          style={{
            fontSize: 12,
            color: "#4ade80",
            background: "rgba(34,197,94,0.1)",
            border: "1px solid rgba(34,197,94,0.2)",
            borderRadius: 20,
            padding: "4px 12px",
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
        >
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              background: "#4ade80",
              display: "inline-block",
              animation: "pulse 2s infinite",
            }}
          />
          API online
        </div>
      </div>

      {/* Linha inferior: estatísticas */}
      <div style={{ display: "flex", gap: 32, padding: "12px 0" }}>
        <Stat
          label="Total de vagas"
          value={totalJobs.toLocaleString("pt-BR")}
          color="#f1f5f9"
        />
        <Stat label="Fontes ativas" value={sources.length} color="#60a5fa" />
        {sources.map((s) => (
          <Stat
            key={s.source}
            label={`Vagas — ${s.source}`}
            value={s.count.toLocaleString("pt-BR")}
            color="#94a3b8"
          />
        ))}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50%       { opacity: 0.4; }
        }
      `}</style>
    </header>
  );
}

function Stat({ label, value, color }) {
  return (
    <div>
      <div
        style={{
          fontSize: 11,
          color: "#475569",
          fontWeight: 600,
          letterSpacing: "0.05em",
          textTransform: "uppercase",
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 20,
          fontWeight: 800,
          color,
          marginTop: 2,
          letterSpacing: "-0.02em",
        }}
      >
        {value}
      </div>
    </div>
  );
}
