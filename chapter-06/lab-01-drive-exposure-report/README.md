# Lab 6.1 Drive and Shared Drive Exposure Report

**Book:** Chapter 6, section "6.1 The Permission Debt You Did Not Know You Had"
**Difficulty:** Level 4 (Secure)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional cloud or Workspace path below
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
An exposure report over Kestrel's Drive and Shared Drives that finds crown-jewel content shared domain-wide or by link, a remediation set, and a DLP rule, then proves the fix.

## Why This Matters
Gemini does not create access. It makes existing access findable in seconds. Permission debt becomes an AI incident the day you switch it on.

## Enterprise Scenario
The 2019 salary review is shared with the whole domain. Nobody broke a rule. Everybody had access.

## Learning Objectives
- Find crown-jewel content with broad sharing
- Remediate before expanding Gemini
- Add a DLP rule for HR content

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
chapter-06/lab-01-drive-exposure-report/
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
python shared/scripts/start-lab.py 6.1
cd workspace/lab-6.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `shared/datasets/kestrel/drive_files.csv`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Write remediation and a DLP rule. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Remediation changes sharing; containment (excluding a Shared Drive from the agent's data store) buys time but needs an owner and an exit date.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
An executive assistant shares next month's board pack by link.
```
python ../../shared/scripts/start-lab.py 6.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `crown-jewel-exposed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.1]"
```

### Optional cloud or Workspace path
Optional (Workspace admin, test OU only): export Drive sharing for a test Shared Drive and compare it with the synthetic format. WORKSPACE VALIDATION REQUIRED.
Use a dedicated sandbox project or test organisational unit, set a budget alert, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (crown-jewel-exposed) |
| After remediation | PASS |

## Evidence
Exposure report before and after remediation. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Non-crown-jewel link shares appear as notes, not blockers.

## Security Considerations
The synthetic model teaches the decision. In a real tenant, use Admin console reports, the Drive audit log and Drive labels.

## Enterprise Application
No Gemini expansion to a new group without a signed exposure report for that group.

## Production Considerations
Alert on new domain or link shares of labelled content.

## Cleanup
Delete `workspace/lab-6.1`. If you used the cloud path, delete the sandbox resources and revoke any key.

## Further Challenge
Add a Legal privilege label and remediate it.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner. Optional cloud or Workspace path: CLOUD VALIDATION REQUIRED.
