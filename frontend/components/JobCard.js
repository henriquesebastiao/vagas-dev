// Cartão de vaga exibido na lista à esquerda.
// Recebe um job, se está selecionado, e a função de clique.

import {
  LEVEL_CONFIG,
  WORKPLACE_CONFIG,
  Badge,
  timeAgo,
} from "@/lib/constants";

export default function JobCard({ job, selected, onClick }) {
  const level = LEVEL_CONFIG[job.level] || {
    bg: "rgba(255,255,255,0.06)",
    text: "#aaa",
    label: job.level,
  };
  const workplace = WORKPLACE_CONFIG[job.workplace_type] || {
    icon: "❓",
    label: job.workplace_type,
  };

  return (
    <div
      onClick={() => onClick(job)}
      style={{
        background: selected
          ? "rgba(99,102,241,0.10)"
          : "rgba(255,255,255,0.03)",
        border: selected
          ? "1px solid rgba(99,102,241,0.5)"
          : "1px solid rgba(255,255,255,0.07)",
        borderRadius: 14,
        padding: "18px 20px",
        cursor: "pointer",
        transition: "all 0.18s ease",
        marginBottom: 10,
        boxShadow: selected ? "0 0 0 2px rgba(99,102,241,0.2)" : "none",
      }}
    >
      {/* Título e tempo */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: 10,
        }}
      >
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontWeight: 700,
              fontSize: 14.5,
              color: "#f1f5f9",
              marginBottom: 4,
              lineHeight: 1.35,
            }}
          >
            {job.title}
          </div>
          <div
            style={{
              fontSize: 13,
              color: "#94a3b8",
              marginBottom: 10,
              fontWeight: 500,
            }}
          >
            {job.company}
          </div>

          {/* Badges de nível, modalidade e PCD */}
          <div
            style={{
              display: "flex",
              gap: 6,
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <Badge bg={level.bg} color={level.text}>
              {level.label}
            </Badge>
            <Badge bg="rgba(255,255,255,0.06)" color="#94a3b8">
              {workplace.icon} {workplace.label}
            </Badge>
            {job.for_pcd && (
              <Badge bg="rgba(251,191,36,0.1)" color="#fbbf24">
                ♿ PCD
              </Badge>
            )}
          </div>
        </div>

        {/* Tempo desde que foi encontrada */}
        <div
          style={{
            fontSize: 11,
            color: "#64748b",
            whiteSpace: "nowrap",
            marginTop: 2,
          }}
        >
          {timeAgo(job.found_at)}
        </div>
      </div>

      {/* Localização */}
      <div
        style={{
          marginTop: 10,
          fontSize: 12,
          color: "#475569",
          display: "flex",
          alignItems: "center",
          gap: 4,
        }}
      >
        <span>📍</span> {job.location || "Não informado"}
      </div>
    </div>
  );
}
