# Lab 8.3 Logging, Detection and the Kill Switch

**Book:** Chapter 8, section "8.3 Logging and Observability"
**Difficulty:** Level 4 (Secure)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
Detection rules over synthetic Cloud Audit Log events, a retention check, and a dated kill switch drill.

## Why This Matters
If the agent did something at 2 a.m., the log is the only witness. If nobody tested the kill switch, it is a hope, not a control.

## Enterprise Scenario
Overnight, the Freight Ops Assistant read 48,210 raw telematics rows, the Procurement Agent created an unapproved order, and someone minted a key. One rule fired.

## Learning Objectives
- Write detections for agent misuse
- Keep agent logs long enough to investigate
- Record a tested kill switch

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
chapter-08/lab-03-logging-detection-kill-switch/
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
python shared/scripts/start-lab.py 8.3
cd workspace/lab-8.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `audit_logs.jsonl`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add detections, raise retention and record the drill. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Data Access audit logs are often off by default for some services. Confirm they are on for the services your agents touch.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A cost-saving change disables the agent log sink.
```
python ../../shared/scripts/start-lab.py 8.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `logging-gap`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (logging-gap) |
| After remediation | PASS |

## Evidence
Alert list and kill switch record. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Every suspicious event must raise at least one alert.

## Security Considerations
Send agent logs to your SIEM (for example Google Security Operations) with the same retention as other privileged activity.

## Enterprise Application
The SOC owns these detections; the platform team owns the log pipeline.

## Production Considerations
Alert on sink changes themselves.

## Cleanup
Delete `workspace/lab-8.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a volume rule for more than 10,000 rows in one query.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
