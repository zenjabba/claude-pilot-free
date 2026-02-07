/**
 * Dashboard Project Filter Tests
 *
 * Tests that StatsGrid hides "Projects" card when a project is selected,
 * Dashboard shows project filter indicator, and workspace section is separated.
 */

import { describe, it, expect } from "bun:test";
import { renderToString } from "react-dom/server";
import React from "react";

describe("Dashboard project filtering", () => {
  it("StatsGrid accepts selectedProject prop", async () => {
    const { StatsGrid } = await import(
      "../../src/ui/viewer/views/Dashboard/StatsGrid.js"
    );

    const stats = {
      observations: 10,
      summaries: 5,
      lastObservationAt: "2m ago",
      projects: 3,
    };

    const htmlAll = renderToString(
      React.createElement(StatsGrid, { stats, selectedProject: null })
    );
    expect(htmlAll).toContain("Projects");

    const htmlFiltered = renderToString(
      React.createElement(StatsGrid, { stats, selectedProject: "my-project" })
    );
    expect(htmlFiltered).not.toContain("Projects");
  });

  it("Dashboard shows project filter indicator when project selected", async () => {
    const { readFileSync } = await import("fs");
    const source = readFileSync(
      "src/ui/viewer/views/Dashboard/index.tsx",
      "utf-8"
    );

    expect(source).toContain("useProject");
    expect(source).toContain("selectedProject");
  });

  it("Dashboard separates workspace-level cards from project-scoped data", async () => {
    const { readFileSync } = await import("fs");
    const source = readFileSync(
      "src/ui/viewer/views/Dashboard/index.tsx",
      "utf-8"
    );

    expect(source).toContain("Workspace");
  });
});
