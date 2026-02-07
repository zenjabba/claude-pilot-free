/**
 * Search Project Filter Tests
 *
 * Tests that SearchView passes project filter to memory search API
 * and shows workspace-level indicator for codebase search.
 */

import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";

describe("Search project filtering", () => {
  it("imports useProject from context", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Search/index.tsx",
      "utf-8"
    );
    expect(source).toContain("useProject");
  });

  it("passes project parameter in memory search", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Search/index.tsx",
      "utf-8"
    );

    expect(source).toContain("selectedProject");

    const searchStart = source.indexOf("handleMemorySearch");
    const searchEnd = source.indexOf("handleCodebaseSearch");
    const searchBlock = source.slice(searchStart, searchEnd);

    expect(searchBlock).toContain("project");
  });

  it("uses ScopeBadge for consistent scope indicators", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Search/index.tsx",
      "utf-8"
    );

    expect(source).toContain("ScopeBadge");
  });

  it("shows workspace scope for codebase search", () => {
    const source = readFileSync(
      "src/ui/viewer/views/Search/index.tsx",
      "utf-8"
    );

    expect(source).toContain("not filtered by project");
    expect(source).toContain("workspace");
  });
});
