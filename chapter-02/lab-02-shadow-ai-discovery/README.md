# Lab 2.2 Shadow AI Discovery

**Book:** Chapter 2, section "2.5 Governing the Sprawl"
**Difficulty:** Level 3 (Integrate)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A reviewed list of third-party AI apps that hold OAuth access to Drive or Gmail, each with a decision and an owner.

## Why This Matters
Shadow AI is not a policy problem. It is an OAuth grant with drive.readonly scope that nobody reviewed.

## Enterprise Scenario
Fourteen Kestrel staff connected an AI meeting-notes app to their Drive. It is not on any register.

## Learning Objectives
- Read an OAuth grant export
- Decide approve, block or review for each AI app
- Assign an owner and a due date

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
chapter-02/lab-02-shadow-ai-discovery/
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
python shared/scripts/start-lab.py 2.2
cd workspace/lab-2.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `shared/datasets/kestrel/oauth_grants.csv`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Record a decision for every unsanctioned AI app with data access.
```
python ../../shared/scripts/start-lab.py 2.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
In the Admin console, app access control can restrict third-party apps by OAuth scope. The lab models that decision.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A new AI slide app appears with Drive read access for 11 users.
```
python ../../shared/scripts/start-lab.py 2.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unreviewed-ai-grant`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: block it and record the owner.
```
python ../../shared/scripts/start-lab.py 2.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[2.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unreviewed-ai-grant) |
| After remediation | PASS |

## Evidence
Grant inventory with decisions. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Sanctioned apps still need an owner.

## Security Considerations
Blocking an app does not delete data it already copied. Ask the vendor and record the answer.

## Enterprise Application
Make the review a weekly control owned by IT and Security.

## Production Considerations
Export grants on a schedule and alert on new AI-category apps.

## Cleanup
Delete `workspace/lab-2.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a rule that blocks any unsanctioned app with gmail scopes automatically.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
