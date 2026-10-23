# Lab 18.1 Portfolio Prioritisation and Executive Dashboard

**Book:** Chapter 18, section "18.3 The Portfolio Prioritisation"
**Difficulty:** Level 8 (Scale)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A prioritised backlog for the next three agents scored on value, risk and effort, a check that each uses the Shared Platform Model, and an Executive Dashboard where every metric has a source.

## Why This Matters
The first agent paid for itself. The next forty will not, unless they share identity, gateway, logging and evaluation.

## Enterprise Scenario
Kestrel's sales team wants its own agent stack with its own identity store and logging.

## Learning Objectives
- Score and rank the backlog
- Enforce reuse of shared components
- Remove dashboard metrics with no system of record

## Prerequisites
- Python 3.11 or later and `python -m pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
Your inputs live in `config.yaml`. Overlays add numbered patch files (`patch-10` solution, `patch-20` break, `patch-30` fix) that are merged in order, so each change is visible and reviewable. A shared engine in `shared/playbook/` applies the checks and writes evidence.
```
config.yaml + patch-*.yaml  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

## Repository Structure
```
chapter-18/lab-01-portfolio-prioritisation-and-dashboard/
  README.md
  lab.json
  starter/
    config.yaml
    run.py
  solution/
    patch-10-solution.yaml
    REMOVE.txt
  lab-changes/
    patch-20-break.yaml
  solution-after-break/
    patch-30-fix.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 18.1
cd workspace/lab-18.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the shared platform, backlog and dashboard.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix reuse and the unsourced metric. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 18.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Every bespoke identity store is another place permissions drift.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Sales submits a bespoke stack.
```
python ../../shared/scripts/start-lab.py 18.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `platform-bypass`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: rebuilt on the shared platform, effort drops.
```
python ../../shared/scripts/start-lab.py 18.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[18.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (platform-bypass) |
| After remediation | PASS |

## Evidence
Ranked backlog and dashboard definition. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- 'Hours saved' without a source is the classic vanity metric.

## Security Considerations
Not applicable beyond platform controls.

## Enterprise Application
The architecture board approves backlog order quarterly.

## Production Considerations
Feed the dashboard from the evidence store and billing export.

## Cleanup
Delete `workspace/lab-18.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a retirement candidate.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
