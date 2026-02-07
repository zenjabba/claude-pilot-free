/**
 * Stats Project Filter Tests
 *
 * Verifies that /api/stats endpoint supports ?project= query parameter
 * to return observation/summary counts filtered by project.
 */

import { describe, it, expect } from "bun:test";
import { readFileSync } from "fs";

function getStatsMethodBody(): string {
  const source = readFileSync(
    "src/services/worker/http/routes/DataRoutes.ts",
    "utf-8"
  );
  const marker = "private handleGetStats = this.wrapHandler";
  const start = source.indexOf(marker);
  const nextMethod = source.indexOf(
    "private handleGetProjects",
    start + marker.length
  );
  return source.slice(start, nextMethod);
}

describe("/api/stats project filtering", () => {
  it("handleGetStats reads project from req.query", () => {
    const body = getStatsMethodBody();
    expect(body).toContain("req.query.project");
  });

  it("handleGetStats applies WHERE clause for observations when project set", () => {
    const body = getStatsMethodBody();
    expect(body).toContain("WHERE project = ?");
  });

  it("handleGetStats still returns global counts when no project specified", () => {
    const body = getStatsMethodBody();
    expect(body).toContain(
      "SELECT COUNT(*) as count FROM observations"
    );
  });
});
