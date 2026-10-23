# Lab 9.1 Use-Case Discovery Canvas and Process Archaeology

**Book:** Chapter 9, section "9.2 Process Archaeology"
**Difficulty:** Level 1 (Explore)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A scored Use-Case Discovery Canvas for three candidate processes, a process archaeology view of the chosen one, and a single selection with an owner and a baseline.

## Why This Matters
The process everyone knows is broken is rarely the one worth proving first. Scoring volume, effort, data readiness and documented rules stops the loudest request winning.

## Enterprise Scenario
Finance wants month-end, People wants onboarding, Operations wants claims. The steering group selected two.

## Learning Objectives
- Score candidates on volume, effort and readiness
- Apply the Single Process Rule
- Confirm owner and baseline before workflow design

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
chapter-09/lab-01-discovery-canvas-and-process-archaeology/
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
python shared/scripts/start-lab.py 9.1
cd workspace/lab-9.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the candidates.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Select one process. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 9.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Process archaeology interviews can surface personal information; record roles, not names.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A second process is quietly added to the pilot.
```
python ../../shared/scripts/start-lab.py 9.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `single-process-rule`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 9.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[9.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (single-process-rule) |
| After remediation | PASS |

## Evidence
Ranked canvas. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A lower-scoring choice needs a written justification.

## Security Considerations
Not applicable beyond document handling.

## Enterprise Application
The winning process feeds Lab 10.1 (workflow design) and Lab 11.1 (pilot).

## Production Considerations
Keep the canvas as the backlog for Lab 18.1.

## Cleanup
Delete `workspace/lab-9.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a fourth candidate from your own organisation and score it.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
