# Lab 15.2 Sovereign Hosting Boundary Check

**Book:** Chapter 15, section "15.3 Sovereignty and the Hosting Boundary"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A check of a synthetic government deployment against the published IRAP in-scope product list, Australian regions and the agency's own authorisation decision.

## Why This Matters
IRAP does not certify a deployment. An IRAP report informs the agency's risk-based authorisation, and product names in the report may not match marketing names.

## Enterprise Scenario
A department wants to use the Gemini Enterprise app with a global model endpoint. The IRAP in-scope list does not name that product.

## Learning Objectives
- Match deployed services to the in-scope list
- Enforce Australian regions for data and model endpoints
- Record the agency's authorisation decision

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
chapter-15/lab-02-sovereign-hosting-boundary-check/
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
python shared/scripts/start-lab.py 15.2
cd workspace/lab-15.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the in-scope list (from Google's IRAP page, October 2026; re-check before use) and the deployment.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix the endpoint, record the confirmation and authorisation. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 15.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Region support for specific models and features varies and changes; confirm in current documentation.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer moves the data store to us-central1 for a preview feature.
```
python ../../shared/scripts/start-lab.py 15.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `residency-breach`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 15.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[15.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (residency-breach) |
| After remediation | PASS |

## Evidence
Deployment check. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A confirmation entry is a record of evidence, not a way to skip the check.

## Security Considerations
Assured Workloads and data residency controls are configuration; verify them, do not assume them.

## Enterprise Application
The agency CISO owns the authorisation decision.

## Production Considerations
Re-run on every service change and on each new IRAP report.

## Cleanup
Delete `workspace/lab-15.2`. No cloud resources are created by the local lab.

## Further Challenge
Add Access Transparency and key management requirements.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
