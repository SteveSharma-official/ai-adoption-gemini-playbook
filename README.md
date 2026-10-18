# AI Adoption Playbook: Google Gemini Labs

Hands-on labs for *The Google Gemini Enterprise Playbook* (Book 2 of the AI Adoption Playbook Series) by Steve Sharma.

The book explains why, what, when, where, who and how. These labs let you show it, build it, test it and validate it, using a fictional
organisation (Kestrel Freight Group, a national logistics company on Google Workspace and BigQuery, with Microsoft 365 in one acquired division)
and synthetic data only. Every lab ends in an evidence pack you could hand to a reviewer.

> Repository: github.com/SteveSharma-official/ai-adoption-gemini-playbook
> Part of the AI Adoption Playbooks series: github.com/SteveSharma-official/ai-adoption-playbooks (series standards, and every book's lab repository as a submodule).

## The learning journey
READ (the chapter) > UNDERSTAND (the concept) > DESIGN > BUILD > TEST > SECURE > GOVERN > VALIDATE > APPLY > SCALE

Every lab follows the same proof sequence: build it, **break it safely**, observe the failure, remediate, **prove the fix**, clean up.

## Quick start
```
python -m pip install -r requirements.txt
python shared/scripts/start-lab.py 0.1
cd workspace/lab-0.1 && python run.py
```
Run every lab's proof sequence from the repository root:
```
python -m pytest -q
```

## Execution paths
| Path | What it needs | Status |
|---|---|---|
| Local (default, every lab) | Python 3.11+, PyYAML, pytest. No API key, no cloud account. | LOCALLY VALIDATED (2026-10-18) |
| Google Cloud (optional: Labs 1.1, 7.2) | A dedicated sandbox project, budget alert, `GEMINI_API_KEY` in the environment | CLOUD VALIDATION REQUIRED |
| Google Workspace (optional: Lab 6.1) | A test organisational unit and admin rights you are authorised to use | CLOUD VALIDATION REQUIRED |

Never point a lab at a production project or tenant. See docs/cloud-sandbox-setup.md and docs/cost-and-cleanup.md.

## Lab index
| Lab | Title | Chapter | Difficulty | Platform | Local sequence (2026-10-18) |
|---|---|---|---|---|---|
| 0.1 | [Quick Start and Lab Safety Check](chapter-00/lab-01-quick-start/) | 0 | 1 (Explore) | Local | Passed |
| 0.2 | [AI Adoption Maturity Self-Assessment](chapter-00/lab-02-maturity-self-assessment/) | 0 | 1 (Explore) | Local | Passed |
| 1.1 | [Grounded Enterprise Assistant Baseline](chapter-01/lab-01-grounded-assistant-baseline/) | 1 | 2 (Build) | Local + optional Google Cloud | Passed |
| 1.2 | [Process Baseline and the 90-Day Plan](chapter-01/lab-02-process-baseline-and-90-day-plan/) | 1 | 5 (Evaluate) | Local | Passed |
| 2.1 | [Enterprise AI Portfolio Map](chapter-02/lab-01-ai-portfolio-map/) | 2 | 2 (Build) | Local | Passed |
| 2.2 | [Shadow AI Discovery](chapter-02/lab-02-shadow-ai-discovery/) | 2 | 3 (Integrate) | Local | Passed |
| 3.1 | [Value Hypothesis and Baseline](chapter-03/lab-01-value-hypothesis-and-baseline/) | 3 | 5 (Evaluate) | Local | Passed |
| 4.1 | [The Decision Ladder](chapter-04/lab-01-decision-ladder/) | 4 | 2 (Build) | Local | Passed |
| 5.1 | [Reference Architecture as Code](chapter-05/lab-01-reference-architecture-as-code/) | 5 | 2 (Build) | Local | Passed |
| 5.2 | [Grounding Boundary and Source Freshness](chapter-05/lab-02-grounding-boundary-test/) | 5 | 5 (Evaluate) | Local | Passed |
| 6.1 | [Drive and Shared Drive Exposure Report](chapter-06/lab-01-drive-exposure-report/) | 6 | 4 (Secure) | Local + optional Workspace | Passed |
| 6.2 | [The Agent's Mirror](chapter-06/lab-02-agents-mirror/) | 6 | 4 (Secure) | Local | Passed |
| 6.3 | [Agent Identity and IAM Audit](chapter-06/lab-03-agent-identity-audit/) | 6 | 4 (Secure) | Local | Passed |
| 7.1 | [Human-Agent Authority Matrix Gateway](chapter-07/lab-01-authority-matrix-gateway/) | 7 | 6 (Govern) | Local | Passed |
| 7.2 | [Gemini Function Calling Behind an Approval Gate](chapter-07/lab-02-gemini-function-calling-approval/) | 7 | 4 (Secure) | Local + optional Gemini API | Passed |
| 8.1 | [Agent Inventory and Register](chapter-08/lab-01-agent-inventory-register/) | 8 | 6 (Govern) | Local | Passed |
| 8.2 | [OWASP Agentic Threat Model](chapter-08/lab-02-owasp-agentic-threat-model/) | 8 | 4 (Secure) | Local | Passed |
| 8.3 | [Logging, Detection and the Kill Switch](chapter-08/lab-03-logging-detection-kill-switch/) | 8 | 4 (Secure) | Local | Passed |
| 9.1 | [Use-Case Discovery Canvas and Process Archaeology](chapter-09/lab-01-discovery-canvas-and-process-archaeology/) | 9 | 1 (Explore) | Local | Passed |
| 10.1 | [Escalation and Failure Paths](chapter-10/lab-01-escalation-and-failure-paths/) | 10 | 5 (Evaluate) | Local | Passed |
| 11.1 | [Pilot Charter and the Day 90 Gate](chapter-11/lab-01-pilot-charter-and-day-90-gate/) | 11 | 6 (Govern) | Local | Passed |
| 12.1 | [Evaluation Harness](chapter-12/lab-01-evaluation-harness/) | 12 | 5 (Evaluate) | Local | Passed |
| 12.2 | [Red Team: Direct and Indirect Prompt Injection](chapter-12/lab-02-red-team-prompt-injection/) | 12 | 4 (Secure) | Local | Passed |
| 12.3 | [Production Readiness Gate](chapter-12/lab-03-production-readiness-gate/) | 12 | 6 (Govern) | Local | Passed |
| 13.1 | [Financial Services Hardship Router and Agentic Audit Trail](chapter-13/lab-01-fs-hardship-router-and-audit-trail/) | 13 | 6 (Govern) | Local | Passed |
| 14.1 | [Clinical Safety Router](chapter-14/lab-01-clinical-safety-router/) | 14 | 6 (Govern) | Local | Passed |
| 15.1 | [Public Authority Line and Transparency Record](chapter-15/lab-01-public-authority-and-transparency-record/) | 15 | 6 (Govern) | Local | Passed |
| 15.2 | [Sovereign Hosting Boundary Check](chapter-15/lab-02-sovereign-hosting-boundary-check/) | 15 | 6 (Govern) | Local | Passed |
| 16.1 | [IT and OT Boundary](chapter-16/lab-01-it-ot-boundary/) | 16 | 4 (Secure) | Local | Passed |
| 16.2 | [Retail Pricing and Refund Rules](chapter-16/lab-02-retail-pricing-and-refund-rules/) | 16 | 6 (Govern) | Local | Passed |
| 17.1 | [Operating Model RACI, Runbook and Kill Switch Drill](chapter-17/lab-01-raci-runbook-and-kill-switch-drill/) | 17 | 7 (Deploy) | Local | Passed |
| 17.2 | [Agent Change Pipeline](chapter-17/lab-02-agent-change-pipeline/) | 17 | 7 (Deploy) | Local | Passed |
| 17.3 | [FinOps Cost Model](chapter-17/lab-03-finops-cost-model/) | 17 | 7 (Deploy) | Local | Passed |
| 18.1 | [Portfolio Prioritisation and Executive Dashboard](chapter-18/lab-01-portfolio-prioritisation-and-dashboard/) | 18 | 8 (Scale) | Local | Passed |
| Capstone | [Enterprise Gemini Adoption Capstone](capstone/enterprise-gemini-adoption/) | 1 to 18 | 8 (Scale) | Local | Passed |

## How a lab is built
```
chapter-06/lab-01-drive-exposure-report/
  README.md        the lab, in the series' standard sections
  lab.json         id, title, expected starter status
  starter/         config.yaml + run.py (your working copy)
  solution/        patch-10-solution.yaml (the reference fix)
  lab-changes/     patch-20-break.yaml (break it safely, INTENTIONALLY INSECURE)
  solution-after-break/  patch-30-fix.yaml (where the fix differs)
```
Patches are merged over `config.yaml` in name order, so every change in the proof sequence is a small file you can read.

## Repository map
| Folder | Purpose |
|---|---|
| `chapter-NN/` | Labs for each chapter (Lab N.N in the book is `chapter-NN/lab-NN-*`) |
| `capstone/enterprise-gemini-adoption/` | End-to-end Day 90 case bringing the labs together |
| `shared/playbook/` | The engine: `core.py` (config, patches, runner), `labs_a.py` (Chapters 0 to 8), `labs_b.py` (9 to 18 and capstone), `common.py` (series evidence format) |
| `shared/datasets/kestrel/` | Synthetic Kestrel Freight Group data (regenerate with `shared/scripts/generate_datasets.py`) |
| `governance/` | Templates used in the book: authority matrix, agent register, RACI, threat model |
| `architecture/` | Reference architecture source for Chapter 5 |
| `docs/` | Getting started, sandbox setup, cost and cleanup, terminology, validation status, troubleshooting |
| `tests/` | The proof sequence test for every lab |

## Validation status
Local proof sequence: **35 of 35 labs passed** on 2026-10-18 (Linux container, Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3). Cloud and Workspace paths and the GitHub Actions workflow have not been executed.
See docs/validation-status.md. A status is never raised without a recorded run.

## Licence and safety
MIT licence. Synthetic data only. Kestrel Freight Group and every person, file and identity in the datasets are fictional.
Product names change: Appendix N of the book and docs/terminology.md record the names current at 2026-10-18.
