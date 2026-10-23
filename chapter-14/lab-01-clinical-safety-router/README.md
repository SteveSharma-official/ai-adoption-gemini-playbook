# Lab 14.1 Clinical Safety Router

**Book:** Chapter 14, section "14.5 The Safety Escalation"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A deterministic router for critical results and an output allowlist that keeps the agent drafting, never deciding.

## Why This Matters
The discharge summary is better written than ever. The clinician still carries the liability, so the clinician still signs.

## Enterprise Scenario
The pilot agent drafted a discharge for a patient with a critical troponin and marked it approved.

## Learning Objectives
- Route critical results to a clinician within a time limit
- Allowlist agent outputs
- Prove no clinical decision is made by the agent

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
chapter-14/lab-01-clinical-safety-router/
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
python shared/scripts/start-lab.py 14.1
cd workspace/lab-14.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read results, router and outputs (synthetic patients).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Set the route and remove the decision output. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Never use real patient data in a lab.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A configuration change lets the agent suggest medication changes.
```
python ../../shared/scripts/start-lab.py 14.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `clinical-decision-by-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[14.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (clinical-decision-by-agent) |
| After remediation | PASS |

## Evidence
Routing table and output review. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Thresholds here are illustrative, not clinical guidance.

## Security Considerations
Clinical content is health information under the Privacy Act and state health records laws.

## Enterprise Application
The CMO signs the Clinical Authority Line.

## Production Considerations
Check whether any function is software as a medical device under TGA rules before go-live; verify current TGA guidance.

## Cleanup
Delete `workspace/lab-14.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a sepsis screening flag.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
