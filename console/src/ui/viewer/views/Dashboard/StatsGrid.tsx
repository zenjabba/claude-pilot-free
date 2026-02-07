import { StatsCard } from './StatsCard';

interface Stats {
  observations: number;
  summaries: number;
  lastObservationAt: string | null;
  projects: number;
}

interface StatsGridProps {
  stats: Stats;
  selectedProject?: string | null;
}

export function StatsGrid({ stats, selectedProject }: StatsGridProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatsCard
        icon="lucide:brain"
        label="Observations"
        value={stats.observations.toLocaleString()}
      />
      <StatsCard
        icon="lucide:clock"
        label="Last Observation"
        value={stats.lastObservationAt || 'None yet'}
      />
      <StatsCard
        icon="lucide:file-text"
        label="Summaries"
        value={stats.summaries.toLocaleString()}
      />
      {!selectedProject && (
        <StatsCard
          icon="lucide:folder"
          label="Projects"
          value={stats.projects.toLocaleString()}
        />
      )}
    </div>
  );
}
