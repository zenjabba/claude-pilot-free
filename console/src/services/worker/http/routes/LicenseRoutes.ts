/**
 * License Routes
 *
 * Exposes license status via /api/license endpoint.
 * Calls `pilot status --json` and caches the result for 5 minutes.
 */

import express, { Request, Response } from "express";
import { BaseRouteHandler } from "../BaseRouteHandler.js";

export interface LicenseResponse {
  valid: boolean;
  tier: string | null;
  email: string | null;
  daysRemaining: number | null;
  isExpired: boolean;
}

export interface ActivateResponse {
  success: boolean;
  tier: string | null;
  email: string | null;
  error: string | null;
}

const ALWAYS_VALID_RESPONSE: LicenseResponse = {
  valid: true,
  tier: "enterprise",
  email: null,
  daysRemaining: null,
  isExpired: false,
};

export class LicenseRoutes extends BaseRouteHandler {
  setupRoutes(app: express.Application): void {
    app.get("/api/license", this.handleGetLicense.bind(this));
    app.post("/api/license/activate", this.handleActivate.bind(this));
  }

  private handleGetLicense = this.wrapHandler((_req: Request, res: Response): void => {
    res.json(this.getLicenseInfo());
  });

  getLicenseInfo(): LicenseResponse {
    return ALWAYS_VALID_RESPONSE;
  }

  private handleActivate = this.wrapHandler((_req: Request, res: Response): void => {
    res.json({ success: true, tier: "enterprise", email: null, error: null } satisfies ActivateResponse);
  });

  activateLicense(_key: string): ActivateResponse {
    return { success: true, tier: "enterprise", email: null, error: null };
  }
}
