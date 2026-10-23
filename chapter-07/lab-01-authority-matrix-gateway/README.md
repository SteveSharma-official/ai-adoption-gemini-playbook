# Lab 7.1 Human-Agent Authority Matrix Gateway

**Book:** Chapter 7, section "7.2 The Human-Agent Authority Matrix"
**Difficulty:** Level 6 (Govern)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A tool gateway that enforces the Human-Agent Authority Matrix: what the agent may do alone, what needs approval, and what stays human-only, including a network rule that the agent can only reach tools through the gateway.

## Why This Matters
The moment the agent can create the purchase order, someone must be able to say who approved it. The matrix answers that question in advance.

## Enterprise Scenario
Kestrel's Procurement Agent created a 48,000 dollar purchase order overnight. Nobody approved it, because nobody decided it needed approval.

## Learning Objectives
- Encode allowed, approval and never actions
- Hold consequential actions above a limit for approval
- Block direct calls that bypass the gateway

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
chapter-07/lab-01-authority-matrix-gateway/
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
python shared/scripts/start-lab.py 7.1
cd workspace/lab-7.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the matrix and requests.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Require approval above 5,000 dollars for purchase orders. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The gateway is only a control if the agent's identity cannot reach the ERP any other way.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer calls the ERP API directly from the agent 'for speed'.
```
python ../../shared/scripts/start-lab.py 7.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `gateway-bypass`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: network policy allows the gateway only (in Google Cloud: VPC Service Controls, private endpoints and IAM on the ERP connector).
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (gateway-bypass) |
| After remediation | PASS |

## Evidence
Decision log for every request. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Drafting is allowed at any amount; executing is not.

## Security Considerations
Keep the matrix in version control and change it through the change pipeline (Lab 17.2).

## Enterprise Application
The CFO and CRO sign the matrix; the engineer implements it.

## Production Considerations
On the Agent Platform, enforce at Agent Gateway or Apigee, and log every decision.

## Cleanup
Delete `workspace/lab-7.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a dual-approval rule above 100,000 dollars.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
