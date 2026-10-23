# Lab 17.2 Agent Change Pipeline

**Book:** Chapter 17, section "17.5 The Change Management Process"
**Difficulty:** Level 7 (Deploy)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A change pipeline for prompts, tools and model versions: pinned versions, evaluation before deployment, and approval for tool changes.

## Why This Matters
An agent changes when its prompt, tools, data or model change. Each change can invalidate last month's evaluation.

## Enterprise Scenario
A tool change shipped without an evaluation run. Then someone switched the model to a 'latest' alias.

## Learning Objectives
- Pin model versions
- Gate deployment on evaluation
- Approve tool changes

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
chapter-17/lab-02-agent-change-pipeline/
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
python shared/scripts/start-lab.py 17.2
cd workspace/lab-17.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the change log.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix CHG-102. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Version names here are placeholders; use the exact model identifiers your platform publishes.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A model alias that floats to the newest version is deployed.
```
python ../../shared/scripts/start-lab.py 17.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unpinned-model`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: pin it and re-run evaluation.
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unpinned-model) |
| After remediation | PASS |

## Evidence
Change table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- `latest` and `auto` aliases are treated as unpinned.

## Security Considerations
Model retirements are scheduled by the vendor; track them in Appendix N.

## Enterprise Application
Agent changes go through the same CAB as other production changes, with evaluation evidence attached.

## Production Considerations
Run Lab 12.1 in CI as the gate.

## Cleanup
Delete `workspace/lab-17.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a data store change type.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
