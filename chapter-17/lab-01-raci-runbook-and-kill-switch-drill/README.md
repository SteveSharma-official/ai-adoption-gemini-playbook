# Lab 17.1 Operating Model RACI, Runbook and Kill Switch Drill

**Book:** Chapter 17, section "17.2 The AI Operating Model RACI"
**Difficulty:** Level 7 (Deploy)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A RACI, a one-page runbook with disable steps, and a dated kill switch drill for each production agent.

## Why This Matters
The agent failed overnight and the person who built it left in March. If the service desk cannot disable it, it is an orphan.

## Enterprise Scenario
Kestrel's Customs Doc Checker is owned by a leaver and has never been drilled.

## Learning Objectives
- Name an accountable person for every agent
- Write disable steps the service desk can follow
- Drill the kill switch every 90 days

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
chapter-17/lab-01-raci-runbook-and-kill-switch-drill/
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
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 17.1
cd workspace/lab-17.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read RACI and runbooks.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix owners, steps and drills. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 17.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Disable steps must work without the builder present.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The Freight Ops Assistant's accountable owner field is changed to a leaver during a restructure.
```
python ../../shared/scripts/start-lab.py 17.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-accountable-owner`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 17.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-accountable-owner) |
| After remediation | PASS |

## Evidence
RACI and drill dates. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Drills older than 90 days fail.

## Security Considerations
Test disable in a sandbox replica first.

## Enterprise Application
Agents join the service catalogue like any other production service.

## Production Considerations
Link runbooks from the Agent Register.

## Cleanup
Delete `workspace/lab-17.1`. No cloud resources are created by the local lab.

## Further Challenge
Add an on-call roster.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
