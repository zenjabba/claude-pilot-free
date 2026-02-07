import { useState, useRef } from 'react';
import { SearchInput } from './SearchInput';
import { SearchResultCard } from './SearchResultCard';
import { CodebaseResultCard } from './CodebaseResultCard';
import { EmptyState, Spinner, Badge, Icon, ScopeBadge } from '../../components/ui';
import { useProject } from '../../context';

type SearchTab = 'memories' | 'codebase';

const SEARCH_TIMEOUT_MS = 120_000;

interface MemorySearchResult {
  id: number;
  type: 'observation' | 'summary' | 'prompt';
  title: string;
  content: string;
  project: string;
  timestamp: string;
  score: number;
  obsType?: string;
}

interface MemorySearchResponse {
  results: MemorySearchResult[];
  query: string;
  usedSemantic: boolean;
  vectorDbAvailable: boolean;
}

interface VexorSearchResult {
  rank: number;
  score: number;
  filePath: string;
  chunkIndex: number;
  startLine: number | null;
  endLine: number | null;
  snippet: string;
}

interface VexorSearchResponse {
  results: VexorSearchResult[];
  query: string;
  error?: string;
}

export function SearchView() {
  const { selectedProject } = useProject();
  const [activeTab, setActiveTab] = useState<SearchTab>('memories');
  const [memoryResults, setMemoryResults] = useState<MemorySearchResult[]>([]);
  const [codebaseResults, setCodebaseResults] = useState<VexorSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [isReindexing, setIsReindexing] = useState(false);
  const [searchMeta, setSearchMeta] = useState<{ usedSemantic: boolean; vectorDbAvailable: boolean } | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const checkReindexStatus = async (): Promise<void> => {
    try {
      const res = await fetch('/api/vexor/status');
      const data = await res.json();
      setIsReindexing(data.isReindexing === true);
    } catch {}
  };

  const handleMemorySearch = async (query: string) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    const timeoutId = setTimeout(() => controller.abort(), SEARCH_TIMEOUT_MS);

    setIsSearching(true);
    setHasSearched(true);
    setSearchError(null);
    try {
      const params = new URLSearchParams({ query, limit: '30' });
      if (selectedProject) {
        params.set('project', selectedProject);
      }
      const response = await fetch(`/api/search/semantic?${params}`, { signal: controller.signal });
      const data: MemorySearchResponse = await response.json();

      setMemoryResults(data.results || []);
      setSearchMeta({
        usedSemantic: data.usedSemantic,
        vectorDbAvailable: data.vectorDbAvailable
      });
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        setSearchError('Search timed out. Please try again.');
      } else {
        setSearchError('Search failed. Please try again.');
      }
      setMemoryResults([]);
      setSearchMeta(null);
    } finally {
      clearTimeout(timeoutId);
      setIsSearching(false);
    }
  };

  const handleCodebaseSearch = async (query: string) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    const timeoutId = setTimeout(() => controller.abort(), SEARCH_TIMEOUT_MS);

    setIsSearching(true);
    setHasSearched(true);
    setSearchError(null);
    setIsReindexing(false);

    const reindexCheckId = setTimeout(() => checkReindexStatus(), 3000);

    try {
      const response = await fetch(`/api/vexor/search?${new URLSearchParams({ query, top: '20' })}`, {
        signal: controller.signal,
      });
      const data: VexorSearchResponse = await response.json();

      if (!response.ok) {
        setSearchError(data.error || `Search failed (${response.status})`);
        setCodebaseResults([]);
      } else {
        setCodebaseResults(data.results || []);
      }
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        setSearchError('Search timed out. The index may be rebuilding — try again in a minute.');
      } else {
        setSearchError('Codebase search failed. Please try again.');
      }
      setCodebaseResults([]);
    } finally {
      clearTimeout(timeoutId);
      clearTimeout(reindexCheckId);
      setIsSearching(false);
      setIsReindexing(false);
    }
  };

  const handleSearch = (query: string) => {
    if (activeTab === 'memories') {
      handleMemorySearch(query);
    } else {
      handleCodebaseSearch(query);
    }
  };

  const handleTabChange = (tab: SearchTab) => {
    abortRef.current?.abort();
    setActiveTab(tab);
    setHasSearched(false);
    setMemoryResults([]);
    setCodebaseResults([]);
    setSearchMeta(null);
    setSearchError(null);
    setIsReindexing(false);
  };

  const placeholder = activeTab === 'memories'
    ? 'Search your memories semantically...'
    : 'Search your codebase files...';

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Search</h1>
        <p className="text-base-content/60">Find memories and code using AI-powered semantic similarity</p>
      </div>

      {/* Tabs with scope indicators */}
      <div role="tablist" className="tabs tabs-bordered">
        <button
          role="tab"
          className={`tab gap-2 ${activeTab === 'memories' ? 'tab-active' : ''}`}
          onClick={() => handleTabChange('memories')}
        >
          <Icon icon="lucide:brain" size={16} />
          Memories
        </button>
        <button
          role="tab"
          className={`tab gap-2 ${activeTab === 'codebase' ? 'tab-active' : ''}`}
          onClick={() => handleTabChange('codebase')}
        >
          <Icon icon="lucide:file-search" size={16} />
          Codebase
        </button>
      </div>

      {/* Scope indicator below tabs */}
      {activeTab === 'memories' ? (
        selectedProject && (
          <div className="flex items-center gap-2">
            <ScopeBadge project={selectedProject} />
          </div>
        )
      ) : (
        <div className="flex items-center gap-2 text-sm text-base-content/50 bg-base-200/50 rounded-lg px-3 py-2">
          <ScopeBadge project={null} workspace />
          {selectedProject && (
            <span className="ml-1">Codebase search covers all workspace files — not filtered by project</span>
          )}
        </div>
      )}

      <SearchInput onSearch={handleSearch} isSearching={isSearching} placeholder={placeholder} />

      {/* Mode indicator */}
      {activeTab === 'memories' && searchMeta && (
        <div className="flex items-center gap-2 text-sm">
          {searchMeta.vectorDbAvailable ? (
            searchMeta.usedSemantic ? (
              <Badge variant="success" outline size="sm">
                <Icon icon="lucide:brain" size={14} className="mr-1" />
                Semantic Search Active
              </Badge>
            ) : (
              <Badge variant="warning" outline size="sm">
                <Icon icon="lucide:filter" size={14} className="mr-1" />
                Filter-only Mode
              </Badge>
            )
          ) : (
            <Badge variant="error" outline size="sm">
              <Icon icon="lucide:alert-triangle" size={14} className="mr-1" />
              Vector DB Unavailable
            </Badge>
          )}
          <span className="text-base-content/50">
            {searchMeta.usedSemantic
              ? 'Results ranked by semantic similarity'
              : searchMeta.vectorDbAvailable
                ? 'Enter a query for semantic ranking'
                : 'Install Chroma for semantic search'}
          </span>
        </div>
      )}

      {activeTab === 'codebase' && hasSearched && !isSearching && !searchError && (
        <div className="flex items-center gap-2 text-sm">
          <Badge variant="info" outline size="sm">
            <Icon icon="lucide:file-search" size={14} className="mr-1" />
            Codebase Search
          </Badge>
          <span className="text-base-content/50">
            Results ranked by semantic similarity to your query
          </span>
        </div>
      )}

      {/* Reindexing notice */}
      {isSearching && isReindexing && (
        <div className="alert alert-warning">
          <Icon icon="lucide:refresh-cw" size={16} className="animate-spin" />
          <span>Index is being rebuilt. This may take a few minutes...</span>
        </div>
      )}

      {/* Error display */}
      {searchError && !isSearching && (
        <div className="alert alert-error">
          <Icon icon="lucide:alert-circle" size={16} />
          <span>{searchError}</span>
        </div>
      )}

      {/* Results */}
      {isSearching ? (
        <div className="flex flex-col items-center justify-center h-64 gap-3">
          <Spinner size="lg" />
          {activeTab === 'codebase' && (
            <span className="text-sm text-base-content/50">Searching codebase...</span>
          )}
        </div>
      ) : !hasSearched ? (
        activeTab === 'memories' ? (
          <EmptyState
            icon="lucide:brain"
            title="Memory Search"
            description="Enter a natural language query to find related memories. Results are ranked by AI-powered similarity matching."
          />
        ) : (
          <EmptyState
            icon="lucide:file-search"
            title="Codebase Search"
            description="Search your codebase files semantically. Find code by describing what it does, not just by keywords."
          />
        )
      ) : searchError ? null : activeTab === 'memories' ? (
        memoryResults.length === 0 ? (
          <EmptyState
            icon="lucide:search-x"
            title="No results found"
            description="Try a different query"
          />
        ) : (
          <div className="space-y-3">
            <div className="text-sm text-base-content/60">
              {memoryResults.length} results
              {searchMeta?.usedSemantic && memoryResults[0]?.score > 0 && (
                <span className="ml-2">
                  (best match: {Math.round(memoryResults[0].score * 100)}% similarity)
                </span>
              )}
            </div>
            {memoryResults.map((result) => (
              <SearchResultCard key={`${result.type}-${result.id}`} result={result} />
            ))}
          </div>
        )
      ) : (
        codebaseResults.length === 0 ? (
          <EmptyState
            icon="lucide:search-x"
            title="No results found"
            description="Try a different query or check that Vexor has indexed your project"
          />
        ) : (
          <div className="space-y-3">
            <div className="text-sm text-base-content/60">
              {codebaseResults.length} results
              {codebaseResults[0]?.score > 0 && (
                <span className="ml-2">
                  (best match: {Math.round(codebaseResults[0].score * 100)}% similarity)
                </span>
              )}
            </div>
            {codebaseResults.map((result) => (
              <CodebaseResultCard key={`${result.filePath}-${result.chunkIndex}`} result={result} />
            ))}
          </div>
        )
      )}
    </div>
  );
}
