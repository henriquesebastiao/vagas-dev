// Painel direito que exibe os detalhes completos da vaga selecionada.
// Quando nenhuma vaga está selecionada, exibe um estado vazio.

import {
  LEVEL_CONFIG,
  WORKPLACE_CONFIG,
  Badge,
  timeAgo,
} from "@/lib/constants";

function InfoCard({ icon, label, value }) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: 12,
        padding: "14px 16px",
      }}
    >
      <div
        style={{
          fontSize: 11,
          color: "#475569",
          fontWeight: 600,
          letterSpacing: "0.05em",
          textTransform: "uppercase",
          marginBottom: 6,
        }}
      >
        {icon} {label}
      </div>
      <div style={{ fontSize: 14, fontWeight: 600, color: "#cbd5e1" }}>
        {value}
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
        color: "#334155",
        gap: 12,
      }}
    >
      <div style={{ fontSize: 48 }}>💼</div>
      <div style={{ fontSize: 16, fontWeight: 600 }}>Selecione uma vaga</div>
      <div style={{ fontSize: 13 }}>
        Clique em uma vaga à esquerda para ver os detalhes
      </div>
    </div>
  );
}

export default function JobDetail({ job }) {
  if (!job)
    return (
      <div style={{ flex: 1, overflowY: "auto", padding: "32px 40px" }}>
        <EmptyState />
      </div>
    );

  const level = LEVEL_CONFIG[job.level] || {
    bg: "rgba(255,255,255,0.07)",
    text: "#aaa",
    label: job.level,
  };
  const workplace = WORKPLACE_CONFIG[job.workplace_type] || {
    icon: "❓",
    label: job.workplace_type,
  };

  // Formata a descrição respeitando quebras de linha
  const descriptionLines = (job.description || "")
    .split("\n")
    .map((line, i) => (
      <span key={i}>
        {line}
        <br />
      </span>
    ));

  return (
    <div style={{ flex: 1, overflowY: "auto", padding: "32px 40px" }}>
      <div style={{ maxWidth: 680 }}>
        {/* Cabeçalho com título e botão de candidatura */}
        <div style={{ marginBottom: 28 }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              gap: 16,
              marginBottom: 12,
            }}
          >
            <h1
              style={{
                fontSize: 24,
                fontWeight: 800,
                color: "#f1f5f9",
                margin: 0,
                letterSpacing: "-0.02em",
                lineHeight: 1.3,
              }}
            >
              {job.title}
            </h1>
            <a
              href={job.url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                background: "linear-gradient(135deg, #6366f1, #0CC0DF)",
                color: "#fff",
                padding: "10px 20px",
                borderRadius: 10,
                textDecoration: "none",
                fontSize: 13,
                fontWeight: 700,
                whiteSpace: "nowrap",
                boxShadow: "0 0 20px rgba(99,102,241,0.3)",
              }}
            >
              Candidatar-se ↗
            </a>
          </div>

          <div
            style={{
              fontSize: 16,
              color: "#94a3b8",
              fontWeight: 600,
              marginBottom: 16,
            }}
          >
            {job.company}
          </div>

          {/* Badges */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <Badge
              bg={level.bg}
              color={level.text}
              fontSize={12}
              padding="5px 12px"
            >
              {level.label}
            </Badge>
            <Badge
              bg="rgba(255,255,255,0.07)"
              color="#94a3b8"
              fontSize={12}
              padding="5px 12px"
            >
              {workplace.icon} {workplace.label}
            </Badge>
            <Badge
              bg="rgba(99,102,241,0.12)"
              color="#818cf8"
              fontSize={12}
              padding="5px 12px"
            >
              via {job.source}
            </Badge>
            {job.for_pcd && (
              <Badge
                bg="rgba(251,191,36,0.1)"
                color="#fbbf24"
                fontSize={12}
                padding="5px 12px"
              >
                ♿ Vaga PCD
              </Badge>
            )}
          </div>
        </div>

        {/* Grid de informações */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 12,
            marginBottom: 28,
          }}
        >
          <InfoCard
            icon="📍"
            label="Localização"
            value={job.location || "Não informado"}
          />
          <InfoCard
            icon="🕐"
            label="Encontrada"
            value={timeAgo(job.found_at)}
          />
        </div>

        {/* Descrição completa */}
        <div
          style={{
            background: "rgba(255,255,255,0.02)",
            border: "1px solid rgba(255,255,255,0.06)",
            borderRadius: 14,
            padding: 24,
          }}
        >
          <div
            style={{
              fontSize: 13,
              fontWeight: 700,
              color: "#475569",
              letterSpacing: "0.05em",
              textTransform: "uppercase",
              marginBottom: 16,
            }}
          >
            Descrição da vaga
          </div>
          <div style={{ color: "#94a3b8", fontSize: 14, lineHeight: 1.8 }}>
            {job.description ? descriptionLines : "Descrição não disponível."}
          </div>
        </div>
      </div>
    </div>
  );
}
