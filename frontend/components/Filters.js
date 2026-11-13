// Barra de filtros. Campos de texto usam debounce para não disparar
// um request a cada tecla.

import { useEffect, useState } from "react";
import { MapPin, Search, X } from "lucide-react";
import { LEVEL_LABELS, SOURCE_LABELS, WORKPLACE_LABELS } from "@/lib/constants";

function useDebounce(value, delay = 350) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

const EMPTY = {
  keyword: "",
  level: "",
  workplace_type: "",
  source: "",
  location: "",
  for_pcd: false,
};

export default function Filters({ onChange, sources = [] }) {
  const [values, setValues] = useState(EMPTY);
  const keyword = useDebounce(values.keyword);
  const location = useDebounce(values.location);

  const set = (key) => (value) => setValues((v) => ({ ...v, [key]: value }));

  const { level, workplace_type, source, for_pcd } = values;

  useEffect(() => {
    onChange({ keyword, level, workplace_type, source, location, for_pcd });
  }, [keyword, level, workplace_type, source, location, for_pcd, onChange]);

  const hasActive = Object.entries(values).some(
    ([key, value]) => value !== EMPTY[key],
  );

  return (
    <div className="filters" role="search">
      <label className="field field--search">
        <Search size={15} aria-hidden="true" />
        <span className="visually-hidden">Buscar no título da vaga</span>
        <input
          id="filter-keyword"
          type="search"
          placeholder="Buscar por cargo ou tecnologia"
          value={values.keyword}
          onChange={(e) => set("keyword")(e.target.value)}
        />
      </label>

      <div className="segmented" role="group" aria-label="Nível">
        <button
          type="button"
          aria-pressed={level === ""}
          onClick={() => set("level")("")}
        >
          Todos os níveis
        </button>
        {Object.entries(LEVEL_LABELS).map(([value, label]) => (
          <button
            key={value}
            type="button"
            aria-pressed={level === value}
            onClick={() => set("level")(level === value ? "" : value)}
          >
            {label}
          </button>
        ))}
      </div>

      <label className="field">
        <span className="visually-hidden">Modalidade</span>
        <select
          id="filter-workplace"
          value={workplace_type}
          onChange={(e) => set("workplace_type")(e.target.value)}
        >
          <option value="">Qualquer modalidade</option>
          {Object.entries(WORKPLACE_LABELS).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span className="visually-hidden">Fonte</span>
        <select
          id="filter-source"
          value={source}
          onChange={(e) => set("source")(e.target.value)}
        >
          <option value="">Todas as fontes</option>
          {sources.map((s) => (
            <option key={s.source} value={s.source}>
              {SOURCE_LABELS[s.source] || s.source}
            </option>
          ))}
        </select>
      </label>

      <label className="field field--location">
        <MapPin size={14} aria-hidden="true" />
        <span className="visually-hidden">Local</span>
        <input
          id="filter-location"
          placeholder="Cidade ou estado"
          value={values.location}
          onChange={(e) => set("location")(e.target.value)}
        />
      </label>

      <label className="check">
        <input
          id="filter-pcd"
          type="checkbox"
          checked={for_pcd}
          onChange={(e) => set("for_pcd")(e.target.checked)}
        />
        Vagas PCD
      </label>

      {hasActive && (
        <button
          type="button"
          className="link-button"
          onClick={() => setValues(EMPTY)}
        >
          <X size={14} aria-hidden="true" />
          Limpar filtros
        </button>
      )}
    </div>
  );
}
