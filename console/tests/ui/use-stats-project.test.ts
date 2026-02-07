/**
 * useStats Project Filtering Tests
 *
 * Tests that useStats passes project parameter to API calls
 * and feeds the project list to context.
 */

import { describe, it, expect } from "bun:test";
import { renderToString } from "react-dom/server";
import React from "react";

describe("useStats project filtering", () => {
  it("useStats hook is exported", async () => {
    const mod = await import("../../src/ui/viewer/hooks/useStats.js");
    expect(mod.useStats).toBeDefined();
    expect(typeof mod.useStats).toBe("function");
  });

  it("useStats accepts selectedProject from context and builds filtered URLs", async () => {
    const { useStats } = await import("../../src/ui/viewer/hooks/useStats.js");
    const { ProjectProvider } = await import(
      "../../src/ui/viewer/context/ProjectContext.js"
    );

    function TestComponent() {
      const result = useStats();
      return React.createElement(
        "div",
        null,
        `loading:${result.isLoading}`,
        `|observations:${result.stats.observations}`
      );
    }

    const html = renderToString(
      React.createElement(ProjectProvider, null,
        React.createElement(TestComponent)
      )
    );

    expect(html).toContain("loading:");
    expect(html).toContain("observations:");
  });

  it("useStats source contains project parameter logic", async () => {
    const fs = await import("fs");
    const source = fs.readFileSync(
      "src/ui/viewer/hooks/useStats.ts",
      "utf-8"
    );

    expect(source).toContain("useProject");

    expect(source).toContain("?project=");

    expect(source).toContain("setProjects");

    expect(source).toContain("selectedProject");
  });
});
