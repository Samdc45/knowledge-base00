# South Consultants Infrastructure & Platform Delivery Plan

This document outlines the step-by-step budgeted plan for delivering the complete South Consultants digital ecosystem. It is based on the current state of the infrastructure (Hetzner server, GitHub repositories, and Base44 apps) and the strategic 12-month roadmap.

## Executive Summary

South Consultants is transitioning from third-party dependencies (Base44, Wix, Vercel) to a fully independent, self-owned infrastructure stack. This transition supports three core platforms:
- **SiteMate (`civilapp.app`)**: Daily site operations and training.
- **SiteGuard (`siteguard.app`)**: Underground asset mapping and strike prevention.
- **TruPeg (`trupeg.app`)**: Survey set-out and variation claims.

The plan is structured into four distinct phases over 12 months, with an estimated total build time of ~157 hours and a stable monthly running cost of ~$75–150 NZD.

## Phase 1: Foundation & SiteMate Stabilisation (Q1)

The immediate priority is to stabilise the existing SiteMate application and secure the foundational infrastructure.

### Current State
- The Hetzner server (`sc-server-01`) is provisioned and running Docker, Portainer, and Nginx.
- DNS records for `southconsultants.biz` are currently caught in a redirect loop and require Nginx configuration fixes.
- SiteMate is live on Base44, but requires payment integration and course viewer updates.

### Action Steps
1.  **Resolve Infrastructure Issues**: Fix the Nginx SSL and redirect loop on the Hetzner server to ensure `southconsultants.biz` and its subdomains (`api`, `hub`) resolve correctly.
2.  **Stripe Integration**: Replace all manual `mailto:` payment links in the SiteMate app with live Stripe checkout links.
3.  **Course Viewer MVP**: Develop a native course viewer within SiteMate to begin the transition away from EdApp.
4.  **Marketing Site Fixes**: Resolve 404 errors on the main marketing site (`/about`, `/products`, `/training`).

### Budget & Effort
- **Estimated Effort**: 29 hours (6 hours Foundation + 23 hours Stabilisation)
- **Running Costs**: ~$12/mo (Hetzner CX32) + ~$40/mo (Supabase Pro)

## Phase 2: Agent Web & SiteGuard MVP (Q2)

With the foundation stable, we will deploy the custom Python AI agent web and launch the first independent platform.

### Action Steps
1.  **Deploy Agent Web**: Launch the 8 core Docker-based agents (Orchestrator, Operations, PA, Course Generation, SiteGuard, TruPeg, Finance, Research) on the Hetzner server, coordinated via Supabase.
2.  **SiteGuard MVP Build**: Develop the SiteGuard application independently (not on Base44).
3.  **API Integrations**: Integrate BYDA/WUAM APIs into the SiteGuard agent for automated underground asset queries.

### Budget & Effort
- **Estimated Effort**: 62 hours (27 hours Agent Web + 35 hours SiteGuard MVP)
- **Running Costs**: Addition of OpenAI API costs (~$20–80/mo depending on agent volume).

## Phase 3: TruPeg MVP & Full Agent Automation (Q3)

This phase focuses on the third platform and ensuring all agents are fully operational.

### Action Steps
1.  **TruPeg MVP Build**: Develop the TruPeg application for survey set-out and scan-to-invoice workflows.
2.  **Hardware Integration**: Explore integration with SDX-PocketScan for point cloud data processing via the TruPeg agent.
3.  **Agent Refinement**: Optimise the Finance and Operations agents based on Q2 data.

### Budget & Effort
- **Estimated Effort**: 42 hours
- **Running Costs**: Stable at ~$75–150/mo total.

## Phase 4: SiteMate Independence (Q4)

The final phase is the complete migration of SiteMate off the Base44 platform.

### Action Steps
1.  **Data Migration**: Migrate all user, course, and operational data from Base44 to the central Supabase instance.
2.  **App Rebuild**: Rebuild the SiteMate frontend to run independently on the Hetzner server.
3.  **Domain Switch**: Point `civilapp.app` to the new independent deployment and decommission the Base44 subscription.

### Budget & Effort
- **Estimated Effort**: 24 hours
- **Running Costs**: Reduction in costs as Base44 is cancelled. Final steady state ~$75–150/mo.

## Resource Allocation Summary

| Phase | Focus Area | Estimated Hours |
|---|---|---|
| Phase 1 | Foundation & Stabilisation | 29 |
| Phase 2 | Agent Web & SiteGuard MVP | 62 |
| Phase 3 | TruPeg MVP & Full Automation | 42 |
| Phase 4 | SiteMate Independence | 24 |
| **Total** | | **~157 Hours** |

## Next Immediate Actions Required from Sam
To proceed with Phase 1, the following items are required:
1.  **API Keys**: Provide OpenAI, Resend, and Stripe Secret keys.
2.  **Supabase Credentials**: Provide the Project URL and `service_role` key from the new Supabase project.
