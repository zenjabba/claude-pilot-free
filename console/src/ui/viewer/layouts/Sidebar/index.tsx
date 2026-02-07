import { SidebarLogo } from './SidebarLogo';
import { SidebarNav } from './SidebarNav';
import { SidebarFooter } from './SidebarFooter';
import { SidebarProjectSelector } from './SidebarProjectSelector';
import { Icon } from '../../components/ui';

interface SidebarProps {
  currentPath: string;
  workerStatus: 'online' | 'offline' | 'processing';
  queueDepth?: number;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export function Sidebar({
  currentPath,
  workerStatus,
  queueDepth,
  collapsed,
  onToggleCollapse,
}: SidebarProps) {
  return (
    <aside
      className={`dashboard-sidebar flex flex-col border-r border-base-300 transition-all duration-300 h-screen sticky top-0 ${
        collapsed ? 'w-[72px]' : 'w-64'
      }`}
    >
      {/* Logo with collapse button - fixed height */}
      <div className="flex-shrink-0 flex items-center justify-between p-4 border-b border-base-300/50">
        {!collapsed && <SidebarLogo />}
        <button
          onClick={onToggleCollapse}
          className="btn btn-ghost btn-sm btn-square"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <Icon icon={collapsed ? 'lucide:panel-left-open' : 'lucide:panel-left-close'} size={18} />
        </button>
      </div>

      {/* Project selector */}
      <SidebarProjectSelector collapsed={collapsed} />

      {/* Navigation */}
      <div className="flex-1">
        <SidebarNav currentPath={currentPath} collapsed={collapsed} />
      </div>

      {/* Footer - fixed at bottom */}
      <div className="flex-shrink-0">
        <SidebarFooter workerStatus={workerStatus} queueDepth={queueDepth} collapsed={collapsed} />
      </div>
    </aside>
  );
}
