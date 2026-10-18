# Lab 11.1 Pilot Charter and the Day 90 Gate

**Book:** Chapter 11, section "11.3 The Day 90 Gate"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A Day 90 Gate decision record that is computed from the charter and the measured evidence: Go, Extend or Stop.

## Why This Matters
Pilots become perpetual when nobody has to decide. The gate forces a decision and the evidence decides which one.

## Enterprise Scenario
Kestrel's claims pilot cut cycle time from 147 to 121 hours against a 110 target. The sponsor wants to announce 'Go'.

## Learning Objectives
- Compute value realised against the target
- Apply safety floors before value
- Record the decision the evidence supports

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
chapter-11/lab-01-pilot-charter-and-day-90-gate/
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
python shared/scripts/start-lab.py 11.1
cd workspace/lab-11.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read charter and measured results.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Correct the recorded decision. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 11.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Safety floors are not negotiable at the gate.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A late evaluation run shows groundedness has fallen below the floor.
```
python ../../shared/scripts/start-lab.py 11.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `gate-decision-unsupported`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: the decision becomes Stop until the fault is fixed.
```
python ../../shared/scripts/start-lab.py 11.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[11.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (gate-decision-unsupported) |
| After remediation | PASS |

## Evidence
Decision record. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Go also requires a signed readiness gate (Lab 12.3).

## Security Considerations
Not applicable.

## Enterprise Application
Communicate Extend and Stop as decisions, not failures.

## Production Considerations
Template the gate pack for every pilot.

## Cleanup
Delete `workspace/lab-11.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a cost floor from Lab 17.3.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
