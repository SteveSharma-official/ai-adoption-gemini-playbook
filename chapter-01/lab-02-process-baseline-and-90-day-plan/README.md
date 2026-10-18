# Lab 1.2 Process Baseline and the 90-Day Plan

**Book:** Chapter 1, section "1.3 The 90-Day Defensible Plan"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A measured baseline for one process, taken from the event log, and a 90-day plan with a dated decision gate.

## Why This Matters
'We will measure it after the pilot' is how a value story dies. The CFO's question in Chapter 1 can only be answered from a baseline taken before the build.

## Enterprise Scenario
Kestrel's claims team believes claims take 'about four days'. The event log for 40 claims says otherwise.

## Learning Objectives
- Compute a process baseline from event data
- Tie the target to the baseline
- Commit the Day 90 Gate to a calendar

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
chapter-01/lab-02-process-baseline-and-90-day-plan/
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
python shared/scripts/start-lab.py 1.2
cd workspace/lab-1.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `shared/datasets/kestrel/claims_process_events.csv`. Run once: the report prints the measured median.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Record the measured baseline in `config.yaml`. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 1.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Event logs can identify customers. Use claim identifiers only.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The sponsor 'removes the gate date for flexibility'.
```
python ../../shared/scripts/start-lab.py 1.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-day-90-gate`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again: the plan keeps its gate date.
```
python ../../shared/scripts/start-lab.py 1.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[1.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-day-90-gate) |
| After remediation | PASS |

## Evidence
Measured baseline and the plan it anchors. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The baseline must be within 10 per cent of the measured value.

## Security Considerations
Aggregate before sharing outside the process team.

## Enterprise Application
No pilot starts without a baseline signed by the business owner.

## Production Considerations
Automate the baseline query so the Day 90 measurement uses the same method.

## Cleanup
Delete `workspace/lab-1.2`. No cloud resources are created by the local lab.

## Further Challenge
Compute the 90th percentile as well as the median and explain which one the CFO should see.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
