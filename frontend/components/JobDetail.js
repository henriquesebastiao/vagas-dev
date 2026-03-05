// Painel direito que exibe os detalhes completos da vaga selecionada.
// Quando nenhuma vaga está selecionada, exibe informações sobre o sistema.

import {
  LEVEL_CONFIG,
  WORKPLACE_CONFIG,
  Badge,
  timeAgo,
} from "@/lib/constants";

import { BriefcaseBusiness } from "lucide-react";

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

function LinkCard({ icon, label, description, href }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "flex",
        alignItems: "center",
        gap: 14,
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: 12,
        padding: "14px 18px",
        textDecoration: "none",
        transition: "all 0.18s",
        cursor: "pointer",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = "rgba(99,102,241,0.08)";
        e.currentTarget.style.borderColor = "rgba(99,102,241,0.3)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = "rgba(255,255,255,0.03)";
        e.currentTarget.style.borderColor = "rgba(255,255,255,0.07)";
      }}
    >
      <span style={{ fontSize: 22 }}>{icon}</span>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: "#e2e8f0",
            marginBottom: 2,
          }}
        >
          {label}
        </div>
        <div style={{ fontSize: 12, color: "#64748b" }}>{description}</div>
      </div>
      <span style={{ color: "#475569", fontSize: 14 }}>↗</span>
    </a>
  );
}

function FeatureItem({ icon, text }) {
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
      <span
        style={{
          fontSize: 15,
          marginTop: 1,
          flexShrink: 0,
        }}
      >
        {icon}
      </span>
      <span style={{ fontSize: 13.5, color: "#94a3b8", lineHeight: 1.6 }}>
        {text}
      </span>
    </div>
  );
}

function WelcomePanel() {
  return (
    <div style={{ flex: 1, overflowY: "auto", padding: "40px 48px" }}>
      <div style={{ maxWidth: 620 }}>
        {/* Logo e título */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            marginBottom: 28,
          }}
        >
          <div>
            <BriefcaseBusiness size={35} color="#fff" />
          </div>
          <div>
            <h1
              style={{
                margin: 0,
                fontSize: 26,
                fontWeight: 800,
                color: "#f1f5f9",
                letterSpacing: "-0.02em",
                lineHeight: 1.2,
              }}
            >
              Vagas DEV
            </h1>
            <p style={{ margin: "4px 0 0", fontSize: 14, color: "#64748b" }}>
              Agregador automático de vagas para desenvolvedores
            </p>
          </div>
        </div>

        {/* Descrição */}
        <div
          style={{
            background: "rgba(99,102,241,0.06)",
            border: "1px solid rgba(99,102,241,0.15)",
            borderRadius: 14,
            padding: "20px 24px",
            marginBottom: 28,
          }}
        >
          <p
            style={{
              margin: 0,
              fontSize: 14,
              color: "#94a3b8",
              lineHeight: 1.8,
            }}
          >
            O <strong style={{ color: "#c7d2fe" }}>Vagas DEV</strong> coleta e
            agrega automaticamente vagas de emprego para desenvolvedores de
            diversas plataformas, eliminando a necessidade de acessar cada site
            separadamente. As vagas são sincronizadas periodicamente e
            notificadas em tempo real via{" "}
            <strong style={{ color: "#c7d2fe" }}>Telegram</strong> e{" "}
            <strong style={{ color: "#c7d2fe" }}>Discord</strong>.
          </p>
        </div>

        {/* Funcionalidades */}
        <div style={{ marginBottom: 28 }}>
          <div
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: "#475569",
              letterSpacing: "0.07em",
              textTransform: "uppercase",
              marginBottom: 14,
            }}
          >
            ✦ Funcionalidades
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <FeatureItem
              icon="🔄"
              text="Sincronização automática a cada 30 minutos com múltiplas fontes de vagas"
            />
            <FeatureItem
              icon="🔔"
              text="Notificações instantâneas no Telegram e Discord com vagas separadas por tecnologia"
            />
            <FeatureItem
              icon="🔍"
              text="Filtros avançados por nível, modalidade, empresa, localização e acessibilidade (PCD)"
            />
            <FeatureItem
              icon="♿"
              text="Identificação e destaque de vagas com cota para pessoas com deficiência"
            />
            <FeatureItem
              icon="🐳"
              text="Deploy simplificado via Docker Compose com um único comando"
            />
          </div>
        </div>

        {/* Links */}
        <div style={{ marginBottom: 28 }}>
          <div
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: "#475569",
              letterSpacing: "0.07em",
              textTransform: "uppercase",
              marginBottom: 14,
            }}
          >
            ✦ Links
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <LinkCard
              icon="📖"
              label="Documentação"
              description="Guia de instalação, configuração e referência da API"
              href="https://henriquesebastiao.github.io/vagas-dev"
            />
            <LinkCard
              icon="💾"
              label="Repositório no GitHub"
              description="Código-fonte, issues e contribuições"
              href="https://github.com/henriquesebastiao/vagas-dev"
            />
            <LinkCard
              icon="🚀"
              label="API REST"
              description="Acesse diretamente os endpoints da API"
              href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
            />
          </div>
        </div>

        {/* Dica de uso */}
        <div
          style={{
            background: "rgba(255,255,255,0.02)",
            border: "1px solid rgba(255,255,255,0.06)",
            borderRadius: 12,
            padding: "16px 20px",
            display: "flex",
            alignItems: "flex-start",
            gap: 12,
          }}
        >
          <span style={{ fontSize: 18, flexShrink: 0 }}>👈</span>
          <p
            style={{
              margin: 0,
              fontSize: 13,
              color: "#64748b",
              lineHeight: 1.7,
            }}
          >
            Selecione uma vaga na lista à esquerda para ver todos os detalhes,
            incluindo descrição completa e link direto para candidatura.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function JobDetail({ job }) {
  if (!job) return <WelcomePanel />;

  const level = LEVEL_CONFIG[job.level] || {
    bg: "rgba(255,255,255,0.07)",
    text: "#aaa",
    label: job.level,
  };
  const workplace = WORKPLACE_CONFIG[job.workplace_type] || {
    icon: "❓",
    label: job.workplace_type,
  };

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
