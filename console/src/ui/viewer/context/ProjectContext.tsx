import { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';

const STORAGE_KEY = 'pilot-memory-selected-project';

interface ProjectContextValue {
  selectedProject: string | null;
  projects: string[];
  setSelectedProject: (project: string | null) => void;
  setProjects: (projects: string[]) => void;
}

const defaultValue: ProjectContextValue = {
  selectedProject: null,
  projects: [],
  setSelectedProject: () => {},
  setProjects: () => {},
};

const ProjectContext = createContext<ProjectContextValue>(defaultValue);

export function ProjectProvider({ children }: { children: ReactNode }) {
  const [selectedProject, setSelectedProjectState] = useState<string | null>(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) || null;
    } catch {
      return null;
    }
  });
  const [projects, setProjectsState] = useState<string[]>([]);

  const setSelectedProject = useCallback((project: string | null) => {
    setSelectedProjectState(project);
    try {
      if (project) {
        localStorage.setItem(STORAGE_KEY, project);
      } else {
        localStorage.removeItem(STORAGE_KEY);
      }
    } catch {}
  }, []);

  const setProjects = useCallback((newProjects: string[]) => {
    setProjectsState(newProjects);
  }, []);

  useEffect(() => {
    fetch('/api/projects')
      .then((res) => res.json())
      .then((data) => {
        const list: string[] = data.projects || [];
        if (list.length > 0) {
          setProjectsState(list);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedProject && projects.length > 0 && !projects.includes(selectedProject)) {
      setSelectedProject(null);
    }
  }, [projects, selectedProject, setSelectedProject]);

  return (
    <ProjectContext.Provider value={{ selectedProject, projects, setSelectedProject, setProjects }}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject(): ProjectContextValue {
  return useContext(ProjectContext);
}
