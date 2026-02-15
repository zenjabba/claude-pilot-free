/**
 * Tests for LicenseRoutes
 *
 * License checking is disabled - routes always return valid enterprise license.
 */
import { describe, it, expect, beforeEach } from "bun:test";

import { LicenseRoutes } from "../../src/services/worker/http/routes/LicenseRoutes.js";

describe("LicenseRoutes", () => {
  let routes: LicenseRoutes;

  beforeEach(() => {
    routes = new LicenseRoutes();
  });

  describe("route setup", () => {
    it("should register GET /api/license", () => {
      const registeredRoutes: string[] = [];
      const mockApp = {
        get: (path: string) => registeredRoutes.push(`GET ${path}`),
        post: (path: string) => registeredRoutes.push(`POST ${path}`),
      };

      routes.setupRoutes(mockApp as any);

      expect(registeredRoutes).toContain("GET /api/license");
    });

    it("should register POST /api/license/activate", () => {
      const registeredRoutes: string[] = [];
      const mockApp = {
        get: (path: string) => registeredRoutes.push(`GET ${path}`),
        post: (path: string) => registeredRoutes.push(`POST ${path}`),
      };

      routes.setupRoutes(mockApp as any);

      expect(registeredRoutes).toContain("POST /api/license/activate");
    });
  });

  describe("getLicenseInfo", () => {
    it("should always return valid enterprise license", () => {
      const result = routes.getLicenseInfo();

      expect(result).toEqual({
        valid: true,
        tier: "enterprise",
        email: null,
        daysRemaining: null,
        isExpired: false,
      });
    });
  });

  describe("activateLicense", () => {
    it("should always return success", () => {
      const result = routes.activateLicense("ANY-KEY");

      expect(result).toEqual({
        success: true,
        tier: "enterprise",
        email: null,
        error: null,
      });
    });
  });
});
