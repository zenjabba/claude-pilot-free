/**
 * Memories Project Filter Tests
 *
 * Tests that MemoriesView uses the global ProjectContext
 * instead of local projectFilter state and URL hash parsing.
 */

import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";

describe("Memories project filtering", () => {
  it("uses useProject from context instead of local state", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Memories/index.tsx",
      "utf-8"
    );

    expect(source).toContain("useProject");

    expect(source).not.toContain("getProjectFromUrl");
    expect(source).not.toContain("setProjectFilter");

    expect(source).not.toContain("hashchange");
  });

  it("uses selectedProject from context in fetch", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Memories/index.tsx",
      "utf-8"
    );

    expect(source).toContain("selectedProject");
  });
});
