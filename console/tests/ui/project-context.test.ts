/**
 * ProjectContext Tests
 *
 * Tests for the project selection context provider and hook.
 * Validates default state, exports, and rendering.
 */

import { describe, it, expect } from "bun:test";
import { renderToString } from "react-dom/server";
import React from "react";

describe("ProjectContext", () => {
  it("exports ProjectProvider and useProject", async () => {
    const mod = await import("../../src/ui/viewer/context/ProjectContext.js");
    expect(mod.ProjectProvider).toBeDefined();
    expect(typeof mod.ProjectProvider).toBe("function");
    expect(mod.useProject).toBeDefined();
    expect(typeof mod.useProject).toBe("function");
  });

  it("exports from context index", async () => {
    const mod = await import("../../src/ui/viewer/context/index.js");
    expect(mod.ProjectProvider).toBeDefined();
    expect(mod.useProject).toBeDefined();
  });

  it("ProjectProvider renders children", async () => {
    const { ProjectProvider } = await import(
      "../../src/ui/viewer/context/ProjectContext.js"
    );

    const html = renderToString(
      React.createElement(
        ProjectProvider,
        null,
        React.createElement("div", null, "child-content")
      )
    );

    expect(html).toContain("child-content");
  });

  it("has stale project validation logic", async () => {
    const fs = await import("fs");
    const source = fs.readFileSync(
      "src/ui/viewer/context/ProjectContext.tsx",
      "utf-8"
    );
    expect(source).toContain("useEffect");
    expect(source).toContain("!projects.includes(selectedProject)");
    expect(source).toContain("setSelectedProject(null)");
  });

  it("useProject returns safe defaults outside provider", async () => {
    const { useProject } = await import(
      "../../src/ui/viewer/context/ProjectContext.js"
    );

    function TestComponent() {
      const ctx = useProject();
      return React.createElement(
        "div",
        null,
        `project:${ctx.selectedProject === null ? "null" : ctx.selectedProject}`,
        `|count:${ctx.projects.length}`
      );
    }

    const html = renderToString(React.createElement(TestComponent));
    expect(html).toContain("project:null");
    expect(html).toContain("count:0");
  });
});
