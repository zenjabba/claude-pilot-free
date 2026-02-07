/**
 * ScopeBadge Tests
 *
 * Tests for the consistent scope indicator component used across views.
 */

import { describe, it, expect } from "bun:test";
import { renderToString } from "react-dom/server";
import React from "react";

describe("ScopeBadge", () => {
  it("renders nothing when project is null and not workspace", async () => {
    const { ScopeBadge } = await import(
      "../../src/ui/viewer/components/ui/ScopeBadge.js"
    );

    const html = renderToString(
      React.createElement(ScopeBadge, { project: null })
    );

    expect(html).toBe("");
  });

  it("renders project name when project is set", async () => {
    const { ScopeBadge } = await import(
      "../../src/ui/viewer/components/ui/ScopeBadge.js"
    );

    const html = renderToString(
      React.createElement(ScopeBadge, { project: "my-app" })
    );

    expect(html).toContain("my-app");
    expect(html).toContain("bg-primary/10");
  });

  it("renders workspace badge when workspace is true", async () => {
    const { ScopeBadge } = await import(
      "../../src/ui/viewer/components/ui/ScopeBadge.js"
    );

    const html = renderToString(
      React.createElement(ScopeBadge, { project: null, workspace: true })
    );

    expect(html).toContain("Workspace");
    expect(html).toContain("bg-base-200");
  });

  it("renders workspace badge even when project is set (workspace takes priority)", async () => {
    const { ScopeBadge } = await import(
      "../../src/ui/viewer/components/ui/ScopeBadge.js"
    );

    const html = renderToString(
      React.createElement(ScopeBadge, { project: "my-app", workspace: true })
    );

    expect(html).toContain("Workspace");
    expect(html).not.toContain("my-app");
  });
});
