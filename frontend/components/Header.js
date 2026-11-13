import { API_URL, SOURCE_LABELS, formatNumber } from "@/lib/constants";

export default function Header({ sources }) {
  const total = sources.reduce((acc, s) => acc + s.count, 0);

  return (
    <header className="topbar">
      <a className="brand" href="./">
        Vagas <span className="brand__suffix">Dev</span>
      </a>

      <div className="topbar__stats mono" aria-label="Vagas indexadas">
        {sources.length > 0 && (
          <>
            <span>
              <strong>{formatNumber(total)}</strong> vagas indexadas
            </span>
            {sources.map((s) => (
              <span key={s.source}>
                {SOURCE_LABELS[s.source] || s.source}{" "}
                <strong>{formatNumber(s.count)}</strong>
              </span>
            ))}
          </>
        )}
      </div>

      <nav className="topbar__nav" aria-label="Links do projeto">
        <a href="https://github.com/henriquesebastiao/vagas-dev">GitHub</a>
        <a href="https://henriquesebastiao.github.io/vagas-dev">Documentação</a>
        <a href={`${API_URL}/`}>API</a>
      </nav>
    </header>
  );
}
