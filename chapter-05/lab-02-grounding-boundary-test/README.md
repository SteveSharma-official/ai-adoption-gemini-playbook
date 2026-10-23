# Lab 5.2 Grounding Boundary and Source Freshness

**Book:** Chapter 5, section "5.3 The Grounding Architecture"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
Tests that prove the HR agent cites the current policy version and refuses when no source covers the question.

## Why This Matters
A grounded agent can still be wrong: it can ground on last year's policy. Freshness is part of the grounding boundary.

## Enterprise Scenario
The People team moved the old leave policy into the same folder 'for reference'. Gemini can now find both versions.

## Learning Objectives
- Test citation of the current version
- Test refusal when no source applies
- See how superseded content poisons answers

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
chapter-05/lab-02-grounding-boundary-test/
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
python shared/scripts/start-lab.py 5.2
cd workspace/lab-5.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `shared/datasets/kestrel/policies.json`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Turn on refusal when silent.
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Use Drive labels or a separate archive Shared Drive outside the agent's data store for superseded documents.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Superseded documents are included in the data store.
```
python ../../shared/scripts/start-lab.py 5.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `stale-source-cited`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again: superseded content is excluded.
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (stale-source-cited) |
| After remediation | PASS |

## Evidence
Transcript with cited versions. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The mock retriever prefers older content on a tie, which is how stale answers appear.

## Security Considerations
Archive is a governance state, not a folder name.

## Enterprise Application
Make policy owners responsible for retiring superseded versions from AI data stores.

## Production Considerations
Add a freshness check to the evaluation suite (Lab 12.1).

## Cleanup
Delete `workspace/lab-5.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a WA-specific question and route it to Lab 10.1's escalation.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
