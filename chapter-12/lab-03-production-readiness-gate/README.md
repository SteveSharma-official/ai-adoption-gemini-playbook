# Lab 12.3 Production Readiness Gate

**Book:** Chapter 12, section "12.4 The Production Readiness Gate"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A Production Readiness Gate that checks every claimed item has an evidence file and a sign-off.

## Why This Matters
'If the CISO is not comfortable, the agent is not ready.' Comfort comes from evidence on file, not a slide that says green.

## Enterprise Scenario
Kestrel's readiness slide is all green. The red team report was never filed and the runbook does not exist.

## Learning Objectives
- Link each gate item to an evidence file
- Require a named sign-off
- Fail on missing evidence

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
chapter-12/lab-03-production-readiness-gate/
  README.md
  lab.json
  starter/
    config.yaml
    run.py
    evidence-store/authority-matrix.md
    evidence-store/evaluation-scorecard.md
    evidence-store/exposure-report.md
    evidence-store/red-team-report.md
  solution/
    patch-10-solution.yaml
    REMOVE.txt
    evidence-store/runbook.md
  lab-changes/
    REMOVE.txt
  solution-after-break/
    evidence-store/red-team-report.md
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 12.3
cd workspace/lab-12.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the checklist and the `evidence-store/` folder.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add the runbook and the missing sign-off. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 12.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Evidence files are copies; keep originals in the records system.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The red team report is deleted during a folder tidy-up.
```
python ../../shared/scripts/start-lab.py 12.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `missing-evidence`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: re-run the red team and file the report.
```
python ../../shared/scripts/start-lab.py 12.3 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (missing-evidence) |
| After remediation | PASS |

## Evidence
Gate result. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- An empty evidence file counts as missing.

## Security Considerations
Evidence may be sensitive; store it with access controls.

## Enterprise Application
This gate is the Day 90 Go precondition (Lab 11.1).

## Production Considerations
Generate the gate from the evidence store automatically.

## Cleanup
Delete `workspace/lab-12.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a hash check against each lab's manifest.json.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
