import { ArrowLeft, ArrowUpRight } from "lucide-react";
import {
  API_URL,
  LEVEL_LABELS,
  SOURCE_LABELS,
  WORKPLACE_LABELS,
  formatDate,
  formatNumber,
  hostOf,
} from "@/lib/constants";

function Intro({ sources }) {
  return (
    <div className="detail intro">
      <h2>Selecione uma vaga para ler os detalhes</h2>
      <p>
        O Vagas Dev consulta a Gupy e o LinkedIn periodicamente e reúne as
        vagas novas nesta lista. As encontradas mais recentemente aparecem
        primeiro.
      </p>

      {sources.length > 0 && (
        <table className="source-table">
          <thead>
            <tr>
              <th scope="col">Fonte</th>
              <th scope="col">Como coletamos</th>
              <th scope="col">Vagas</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((s) => (
              <tr key={s.source}>
                <td>{SOURCE_LABELS[s.source] || s.source}</td>
                <td>
                  {s.source === "gupy" ? "API pública" : "Página de busca"}
                </td>
                <td className="mono">{formatNumber(s.count)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <ul className="intro-links">
        <li>
          <a href="https://henriquesebastiao.github.io/vagas-dev">
            Documentação <ArrowUpRight size={14} aria-hidden="true" />
          </a>
        </li>
        <li>
          <a href="https://github.com/henriquesebastiao/vagas-dev">
            Código no GitHub <ArrowUpRight size={14} aria-hidden="true" />
          </a>
        </li>
        <li>
          <a href={`${API_URL}/`}>
            Referência da API <ArrowUpRight size={14} aria-hidden="true" />
          </a>
        </li>
      </ul>
    </div>
  );
}

export default function JobDetail({ job, sources, onBack }) {
  if (!job) return <Intro sources={sources} />;

  const source = SOURCE_LABELS[job.source] || job.source;
  const facts = [
    ["Nível", LEVEL_LABELS[job.level] || "Não informado"],
    ["Modalidade", WORKPLACE_LABELS[job.workplace_type] || "Não informada"],
    ["Local", job.location || "Não informado"],
    ["Publicada em", formatDate(job.published_at)],
    ["Inscrições até", formatDate(job.end_applications)],
    ["Encontrada em", formatDate(job.found_at)],
  ];

  return (
    <article className="detail">
      <button
        type="button"
        className="link-button detail__back"
        onClick={onBack}
      >
        <ArrowLeft size={15} aria-hidden="true" />
        Voltar para a lista
      </button>

      <div className="detail__company">
        {job.company || "Empresa não informada"}
      </div>
      <h1 className="detail__title">{job.title}</h1>

      <div className="detail__actions">
        <a
          className="button-primary"
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Candidatar-se
          <ArrowUpRight size={16} aria-hidden="true" />
        </a>
        <span className="detail__host mono">{hostOf(job.url)}</span>
        {job.for_pcd && <em className="tag tag--accent">Vaga PCD</em>}
      </div>

      <dl className="facts">
        {facts.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>

      <h2 className="section-label">Descrição</h2>
      {job.description ? (
        <div className="description">{job.description}</div>
      ) : (
        <p className="description description--empty">
          A descrição não está disponível para vagas coletadas de {source}. Leia
          os requisitos completos na página da vaga.
        </p>
      )}

      <p className="provenance mono">
        fonte: {job.source}
        {job.external_id && ` · id externo: ${job.external_id}`}
        {job.keyword && ` · encontrada pela busca "${job.keyword}"`}
      </p>
    </article>
  );
}
