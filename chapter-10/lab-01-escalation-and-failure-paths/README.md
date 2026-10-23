# Lab 10.1 Escalation and Failure Paths

**Book:** Chapter 10, section "10.3 Designing the Escalation Path"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
An escalation design for the HR agent, tested against edge cases: a different state award, low confidence and a wellbeing disclosure.

## Why This Matters
The happy path is easy. Production quality is decided by what the agent does with the question it should not answer.

## Enterprise Scenario
The HR agent answers leave questions well, until a WA employee asks about parental leave under a different award.

## Learning Objectives
- Define escalation triggers
- Name a human queue with a service level
- Test that 'I don't know' happens when it should

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
chapter-10/lab-01-escalation-and-failure-paths/
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
python shared/scripts/start-lab.py 10.1
cd workspace/lab-10.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the agent settings and tests.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Set triggers and a target. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 10.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Wellbeing and complaint disclosures always reach a person, regardless of confidence.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone lowers the confidence threshold to reduce escalations.
```
python ../../shared/scripts/start-lab.py 10.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unsafe-answer`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 10.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[10.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unsafe-answer) |
| After remediation | PASS |

## Evidence
Test results and escalation rate. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Over-escalation is a note, not a failure, but watch the rate.

## Security Considerations
Escalation messages should carry context without copying sensitive content into chat logs.

## Enterprise Application
People Advisory signs the triggers.

## Production Considerations
Report escalation rate weekly; a sudden drop is a warning sign.

## Cleanup
Delete `workspace/lab-10.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a test for a casual employee and decide the trigger.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
