/**
 * Sessions Project Filter Tests
 *
 * Tests that SessionsView uses the global ProjectContext
 * instead of local project state and dropdown.
 */

import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";

describe("Sessions project filtering", () => {
  it("uses useProject from context instead of local state", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Sessions/index.tsx",
      "utf-8"
    );

    expect(source).toContain("useProject");

    expect(source).not.toContain("setProjectFilter");
    expect(source).not.toContain("fetchProjects");

    expect(source).toContain("selectedProject");
  });

  it("removes local project Select dropdown", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Sessions/index.tsx",
      "utf-8"
    );

    expect(source).not.toContain("projectOptions");
    expect(source).not.toContain('<Select');
  });
});
