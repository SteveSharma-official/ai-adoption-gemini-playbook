# Terminology

These terms are used identically in the book and in this repository.

| Term | Meaning | Book chapter | Lab |
|---|---|---|---|
| Gemini Value Chain | Identify, Workspace and data, grounding design, Gemini or Agent Platform, IAM and data governance, pilot, scale (Book 2 form of the series AI Adoption Value Chain) | 0 | All |
| AI Adoption Maturity Model | Five levels (Experiment, Controlled pilot, Operational, Scaled, Agentic enterprise), each gated by evidence | 0 | 0.2 |
| Decision Ladder | Buy, Configure, Integrate, Build, Host | 0, 4 | 4.1 |
| Enterprise AI Portfolio Map | Places each workload on a platform by data location, with identity boundaries and connector justifications | 2 | 2.1 |
| Value Hypothesis | Business metric, measured baseline, target, system of record, owner | 3 | 1.2, 3.1 |
| Grounding Architecture | Approved sources only, citation required, refusal when the source is silent, freshness enforced | 5 | 1.1, 5.2 |
| Three Layers of Gemini Enterprise | Productivity (Gemini in Workspace), agent experience (Gemini Enterprise app), build and run (Gemini Enterprise Agent Platform) | 5 | 5.1 |
| Permission Debt | Accumulated broad sharing that an agent makes discoverable | 6 | 6.1 |
| The Agent's Mirror | An agent surfaces exactly what the asking user can access | 6 | 6.2 |
| Scoped Agent Identity | A dedicated, least-privilege identity per agent with an owner | 6 | 6.3 |
| Action Boundary | The point where an agent stops answering and starts acting | 7 | 7.1, 7.2 |
| Human-Agent Authority Matrix | Per action: allowed, approval (with limits) or never | 7 | 7.1, 7.2 |
| Approval Gate | Execution held until a human approval token exists | 7 | 7.1, 7.2 |
| Agent Register | The authoritative list of agents with owners and risk tiers (Agent Inventory is the discovery step) | 8 | 8.1 |
| Kill Switch | Tested procedure to disable an agent and revoke its access | 8, 17 | 8.3, 17.1 |
| Use-Case Discovery Canvas | Scores candidate processes on volume, effort, data readiness and documented rules | 9 | 9.1 |
| Process Archaeology | Reconstructing how a process actually runs from events and interviews | 9 | 9.1 |
| Single Process Rule | Prove one process before you pilot three | 9 | 9.1 |
| Escalation Path | Named human queue, triggers and service level for questions the agent must not answer | 10 | 10.1 |
| Day 90 Gate | Evidence-based Go, Extend or Stop decision | 11 | 11.1 |
| Evaluation Harness | Scored test set (task success, groundedness, safety, escalation) with regression checks | 12 | 12.1 |
| Production Readiness Gate | Every gate item backed by evidence on file and a named sign-off | 8, 12 | 12.3 |
| Human Authority Line | Sector form of the authority matrix: Credit (13), Clinical (14), Public (15) | 13 to 15 | 13.1, 14.1, 15.1 |
| Agentic Audit Trail | Hash-chained, tamper-evident record of agent actions and routing | 13 | 13.1 |
| Transparency Record | Public record of how AI is used in a government decision process | 15 | 15.1 |
| Sovereign AI Boundary | Region, IRAP scope and agency authorisation for a deployment | 15 | 15.2 |
| AI Operating Model RACI | Accountable and responsible people for every production agent | 17 | 17.1 |
| Agent Runbook | One page: disable steps, contacts, drill date | 17 | 17.1 |
| Shared Platform Model | Identity pattern, gateway, logging, evaluation and data governance reused by every agent | 18 | 18.1 |
| Executive Dashboard | Business metrics, each with a system of record and owner | 18 | 18.1 |
| Evidence pack | result.json, report.md and manifest.json (SHA-256) produced by every lab | 0 | All |
| Kestrel Freight Group (fictional) | The synthetic organisation used in every lab | 0 | All |

## Platform names current at 2026-10-18 (volatile)
The labs model capabilities, not products. These names were checked on 2026-10-18; the book's Appendix N is the living record.

| Name | Note |
|---|---|
| Gemini Enterprise (formerly Google Agentspace) | Rebranded October 2025 |
| Gemini Enterprise Agent Platform (the evolution of Vertex AI) | Announced at Google Cloud Next, week of 23 April 2026 |
| Agent Studio, Agent Development Kit (ADK), Agent Runtime, Agent Sandbox, Agent Memory Bank | Agent Platform components named in Google's Next '26 wrap-up (24 April 2026) |
| Agent Identity, Agent Registry, Agent Gateway, Model Armor, Agent Security dashboard | Security components named in the same wrap-up; some features were in preview |
| OWASP Top 10 for Agentic Applications (ASI01 to ASI10) | Published 9 December 2025 |
