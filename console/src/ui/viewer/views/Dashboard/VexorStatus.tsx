import { useState } from 'react';
import { Card, CardBody, CardTitle, Badge, Icon } from '../../components/ui';

interface VexorStatusProps {
  isIndexed: boolean;
  files: number;
  generatedAt: string | null;
  isReindexing: boolean;
}

function formatIndexAge(generatedAt: string | null): string {
  if (!generatedAt) return 'Never';
  try {
    const date = new Date(generatedAt);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return `${Math.floor(diff / 86400000)}d ago`;
  } catch {
    return 'Unknown';
  }
}

export function VexorStatus({ isIndexed, files, generatedAt, isReindexing }: VexorStatusProps) {
  const [localReindexing, setLocalReindexing] = useState(false);
  const reindexActive = isReindexing || localReindexing;

  const handleReindex = async () => {
    setLocalReindexing(true);
    try {
      const res = await fetch('/api/vexor/reindex', { method: 'POST' });
      if (!res.ok) {
        const data = await res.json();
        console.error('Reindex failed:', data.error);
      }
    } catch (error) {
      console.error('Reindex request failed:', error);
    }

    const poll = setInterval(async () => {
      try {
        const res = await fetch('/api/vexor/status');
        const data = await res.json();
        if (!data.isReindexing) {
          clearInterval(poll);
          setLocalReindexing(false);
        }
      } catch {
        clearInterval(poll);
        setLocalReindexing(false);
      }
    }, 5000);
  };

  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <CardTitle>Codebase Indexing</CardTitle>
            <Badge variant="ghost" size="sm">Workspace</Badge>
          </div>
          {reindexActive ? (
            <Badge variant="warning">
              <Icon icon="lucide:refresh-cw" size={12} className="mr-1 animate-spin" />
              Indexing...
            </Badge>
          ) : (
            <Badge variant={isIndexed ? 'success' : 'warning'}>
              {isIndexed ? 'Indexed' : 'Not Indexed'}
            </Badge>
          )}
        </div>
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm">
            <Icon icon="lucide:file-search" size={16} className="text-base-content/50" />
            <span className="text-base-content/70">Files:</span>
            <span className="font-semibold">{files.toLocaleString()}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Icon icon="lucide:clock" size={16} className="text-base-content/50" />
            <span className="text-base-content/70">Last indexed:</span>
            <span>{formatIndexAge(generatedAt)}</span>
          </div>
        </div>
        <div className="mt-4">
          <button
            className="btn btn-sm btn-outline gap-2"
            onClick={handleReindex}
            disabled={reindexActive}
          >
            <Icon icon="lucide:refresh-cw" size={14} className={reindexActive ? 'animate-spin' : ''} />
            {reindexActive ? 'Rebuilding Index...' : 'Re-index'}
          </button>
        </div>
      </CardBody>
    </Card>
  );
}
