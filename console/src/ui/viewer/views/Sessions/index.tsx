import { useState, useEffect, useCallback } from 'react';
import { SessionCard } from './SessionCard';
import { SessionTimeline } from './SessionTimeline';
import { EmptyState, Spinner, Button, Icon, ScopeBadge } from '../../components/ui';
import { useProject } from '../../context';

interface Session {
  id: number;
  content_session_id: string;
  memory_session_id: string;
  project: string;
  user_prompt: string;
  started_at: string;
  started_at_epoch: number;
  completed_at: string | null;
  completed_at_epoch: number | null;
  status: string;
  observation_count: number;
  prompt_count: number;
}

export function SessionsView() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSessionId, setSelectedSessionId] = useState<number | null>(null);
  const { selectedProject } = useProject();

  const fetchSessions = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      params.set('limit', '50');
      if (selectedProject) {
        params.set('project', selectedProject);
      }

      const response = await fetch(`/api/sessions?${params}`);
      const data = await response.json();
      setSessions(data.items || []);
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    } finally {
      setIsLoading(false);
    }
  }, [selectedProject]);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  const handleSelectSession = (id: number) => {
    setSelectedSessionId(selectedSessionId === id ? null : id);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold">Sessions</h1>
            <ScopeBadge project={selectedProject} />
          </div>
          <p className="text-base-content/60">Browse sessions and explore their timeline</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={fetchSessions}>
            <Icon icon="lucide:refresh-cw" size={16} />
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <Spinner size="lg" />
        </div>
      ) : sessions.length === 0 ? (
        <EmptyState
          icon="lucide:history"
          title="No sessions found"
          description="Sessions will appear here as you use Claude Code"
        />
      ) : (
        <div className="space-y-4">
          {sessions.map((session) => (
            <div key={session.id}>
              <SessionCard
                session={session}
                isExpanded={selectedSessionId === session.id}
                onToggle={() => handleSelectSession(session.id)}
              />
              {selectedSessionId === session.id && (
                <SessionTimeline sessionId={session.id} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
