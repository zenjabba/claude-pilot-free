import { Icon } from './Icon';

interface ScopeBadgeProps {
  /** When set, shows the project name as a filtered badge. When null, shows nothing (all projects). */
  project: string | null;
  /** If true, this view is workspace-level and ignores project filter. */
  workspace?: boolean;
}

/**
 * Consistent scope indicator across all views.
 * Shows either a project-filtered badge or a workspace badge.
 */
export function ScopeBadge({ project, workspace = false }: ScopeBadgeProps) {
  if (workspace) {
    return (
      <span className="inline-flex items-center gap-1 text-xs bg-base-200 text-base-content/50 rounded-full px-2.5 py-0.5">
        <Icon icon="lucide:globe" size={12} />
        Workspace
      </span>
    );
  }

  if (!project) return null;

  return (
    <span className="inline-flex items-center gap-1 text-xs bg-primary/10 text-primary rounded-full px-2.5 py-0.5">
      <Icon icon="lucide:folder" size={12} />
      {project}
    </span>
  );
}
