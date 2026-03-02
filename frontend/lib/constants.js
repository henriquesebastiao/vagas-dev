// Configurações visuais e helpers compartilhados entre componentes.

export const LEVEL_CONFIG = {
  junior: { bg: "rgba(34,197,94,0.12)", text: "#4ade80", label: "Júnior" },
  pleno: { bg: "rgba(59,130,246,0.12)", text: "#60a5fa", label: "Pleno" },
  senior: { bg: "rgba(168,85,247,0.12)", text: "#c084fc", label: "Sênior" },
  estagio: { bg: "rgba(251,191,36,0.12)", text: "#fbbf24", label: "Estágio" },
  trainee: { bg: "rgba(251,146,60,0.12)", text: "#fb923c", label: "Trainee" },
};

export const WORKPLACE_CONFIG = {
  remote: { icon: "🌐", label: "Remoto" },
  hybrid: { icon: "🔀", label: "Híbrido" },
  "on-site": { icon: "🏢", label: "Presencial" },
};

/** Transforma uma data ISO em tempo relativo legível. */
export function timeAgo(dateStr) {
  const diff = Math.floor((Date.now() - new Date(dateStr)) / 60000);
  if (diff < 60) return `${diff}min atrás`;
  if (diff < 1440) return `${Math.floor(diff / 60)}h atrás`;
  return `${Math.floor(diff / 1440)}d atrás`;
}

/** Componente Badge reutilizável para tags coloridas. */
export function Badge({
  children,
  bg,
  color,
  fontSize = 11,
  padding = "3px 9px",
}) {
  return (
    <span
      style={{
        fontSize,
        fontWeight: 600,
        letterSpacing: "0.04em",
        padding,
        borderRadius: 20,
        background: bg,
        color,
      }}
    >
      {children}
    </span>
  );
}
