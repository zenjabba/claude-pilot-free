import { Icon, Tooltip } from '../../components/ui';
import { useProject } from '../../context';

interface SidebarProjectSelectorProps {
  collapsed?: boolean;
}

export function SidebarProjectSelector({ collapsed = false }: SidebarProjectSelectorProps) {
  const { selectedProject, projects, setSelectedProject } = useProject();

  if (collapsed) {
    return (
      <div className="flex-shrink-0 px-3 py-3 border-b border-base-300/50">
        <Tooltip text={selectedProject ?? 'All Projects'}>
          <button
            className={`btn btn-ghost btn-sm btn-square w-full ${selectedProject ? 'text-primary' : 'text-base-content/50'}`}
            onClick={() => setSelectedProject(null)}
          >
            <Icon icon="lucide:folder-open" size={20} />
          </button>
        </Tooltip>
      </div>
    );
  }

  return (
    <div className="flex-shrink-0 px-3 py-3 border-b border-base-300/50 relative z-10">
      <label className="text-[10px] font-semibold uppercase tracking-wider text-base-content/40 px-1 mb-1.5 block">
        Project
      </label>
      <select
        className="select select-bordered select-sm w-full text-sm bg-base-100"
        value={selectedProject ?? ''}
        onChange={(e) => setSelectedProject(e.target.value || null)}
      >
        <option value="">All Projects</option>
        {projects.map((p) => (
          <option key={p} value={p}>{p}</option>
        ))}
      </select>
    </div>
  );
}
