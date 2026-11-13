import {
  LEVEL_LABELS,
  SOURCE_LABELS,
  WORKPLACE_LABELS,
  timeAgo,
} from "@/lib/constants";

export default function JobCard({ job, selected, onSelect }) {
  const meta = [
    LEVEL_LABELS[job.level],
    WORKPLACE_LABELS[job.workplace_type],
    job.location,
  ].filter(Boolean);

  return (
    <button
      type="button"
      className="job-row"
      aria-current={selected ? "true" : undefined}
      onClick={() => onSelect(job)}
    >
      <div>
        <div className="job-row__company">
          {job.company || "Empresa não informada"}
        </div>
        <div className="job-row__title">{job.title}</div>
        <div className="job-row__meta">
          {meta.map((item) => (
            <span key={item}>{item}</span>
          ))}
          {job.for_pcd && <em className="tag tag--accent">PCD</em>}
        </div>
      </div>
      <div className="job-row__aside">
        <span className="tag">{SOURCE_LABELS[job.source] || job.source}</span>
        <time className="mono" dateTime={job.found_at}>
          {timeAgo(job.found_at)}
        </time>
      </div>
    </button>
  );
}
