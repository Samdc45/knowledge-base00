# Architecture & Engineering Memory: April 28, 2026

This document captures the key architectural decisions, bug fixes, and new workflows implemented during the engineering session on April 28, 2026. It serves as persistent memory for the agent swarm, Orchestrator, and Manus to understand the current state of the South Consultants infrastructure.

## 1. Sub-Agent Command Architecture (Directed Autonomy)

We transitioned the agent swarm from pure **scheduled autonomy** (running on cron timers) to **directed autonomy**. Manus and Orchestrator can now dispatch tasks to specific agents in real time.

### How it works:
1. Manus or Orchestrator sends a `POST` request to the webhook agent at `http://204.168.183.104:4000/command`.
2. The payload includes `agent`, `task_type`, `payload`, and `source`.
3. The webhook writes the task to the `agent_tasks` table in Supabase.
4. The target agent (e.g., Research, Sales) polls `agent_tasks` every 60 seconds, picks up the task, executes it, and updates the status.

**Key learning:** The `source` and `updated_at` columns do not exist natively on the `agent_tasks` table schema. When dispatching tasks, the `source` must be nested inside the JSON `payload` field, and `updated_at` should be omitted from the insert object.

## 2. Agent Report Review System

To provide Sam with oversight and feedback loops, all agents now post their autonomous cycle reports to a centralized review queue.

### The Flow:
- **Research Agent:** Posts weekly intelligence reports (leads and tenders found).
- **Operations Agent:** Posts daily SiteMate briefings (hazards, check-ins, overdue machines).
- **Finance Agent:** Posts weekly Stripe revenue and churn summaries.
- **Sales Agent:** Posts daily outreach pipeline results.
- **Orchestrator:** Posts peer review feedback results.

All reports are inserted into the `agent_reports` Supabase table with `status = 'pending_review'`. The SC Hub desktop app fetches these via `GET /reports` on the webhook, displaying them in dedicated agent tabs. Sam can approve, reject, or comment on them via `PATCH /reports/:id`.

**Key learning:** Not all agents have the `supabase_insert` helper function defined identically. When patching agents, always verify the local helper function name (e.g., Operations uses `HEADERS` instead of `SUPABASE_HEADERS`, Finance lacked the helper entirely).

## 3. Critical Bug Fixes

### Research Agent: Grok API Deprecation
- **Symptom:** Research Agent returned 0 leads.
- **Root Cause:** The agent was calling Grok with `search_parameters: {mode: on}`, which is a deprecated live search parameter that causes the API to return an error.
- **Fix:** Removed the `search_parameters` block entirely. The agent now successfully extracts leads (e.g., SEE Group, DT Infrastructure).

### Research Agent: LLM Fallback Chain
- **Symptom:** Suboptimal extraction quality.
- **Fix:** Rewired the fallback chain to prioritize OpenAI first, then DeepSeek, then Grok. Added strict JSON validation before accepting the LLM response.

### Supabase Schema: `sales_leads` Table
- **Symptom:** Leads were extracted but not saved to Supabase.
- **Root Cause:** The `sales_leads` table was missing 5 columns that the Research Agent was trying to insert: `website`, `signal`, `source_url`, `pitch_angle`, `extracted_by`, `researched_at`.
- **Fix:** Ran `ALTER TABLE` to add the missing columns.

### Bridge Agent: `execution_proofs` Table
- **Symptom:** Bridge Agent threw Supabase errors on startup.
- **Root Cause:** The `execution_proofs` table did not exist.
- **Fix:** Created the table via the Supabase SQL Editor with RLS enabled and a `service_role` policy.

## 4. Systems Engineer Recommendations

The Systems Engineer agent ran a self-engineering cycle and produced 6 key recommendations. The top priority (Phase 1) is to implement **Container Resource Limits** to prevent the Ollama container from starving the rest of the swarm during heavy inference.

The second priority is migrating from Nginx to **Traefik** for automatic SSL management and dynamic routing, aligning with the infrastructure independence strategy.

## 5. Webhook HTTP Client Pattern

The webhook agent (`sc-webhook/src/index.js`) does not use `axios` for outbound requests. It relies entirely on the native Node.js `http` and `https` modules.

**Key learning:** When adding new endpoints that require outbound API calls (like Supabase inserts), you must use the native `https.request` pattern or build a wrapper like `supabaseRequest()`. Attempting to `require('axios')` will crash the container.
