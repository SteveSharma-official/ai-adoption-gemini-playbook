# Lab 12.1 Evaluation Harness

**Book:** Chapter 12, section "12.2 Building the Evaluation Harness"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 90 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
An evaluation harness over 70 cases (40 core, 10 safety, 20 edge) that scores task success, groundedness, safety and escalation, compares with the last release and fails on regression.

## Why This Matters
The demo used twelve hand-picked questions. An evaluation set is how you know the agent works on the questions you did not pick.

## Enterprise Scenario
Kestrel's claims agent scores well on the demo set and misses two edge-case escalations in the full set.

## Learning Objectives
- Score four metrics by category
- Set thresholds by risk tier
- Fail a release on regression

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
chapter-12/lab-01-evaluation-harness/
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
python shared/scripts/start-lab.py 12.1
cd workspace/lab-12.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the test set, thresholds and responses.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix the failing responses (in reality, the agent). Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Safety and escalation thresholds are 100 per cent for this risk tier; these are author recommendations, not standards.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A prompt change drops task success from 97.5 to 92.5 per cent.
```
python ../../shared/scripts/start-lab.py 12.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `regression`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again (in reality: roll back the change).
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (regression) |
| After remediation | PASS |

## Evidence
`scores.json` and the scorecard. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Groundedness here means the answer is supported by a cited source; review each failure before calling it a hallucination.

## Security Considerations
Keep evaluation data synthetic or de-identified.

## Enterprise Application
No release without a scorecard.

## Production Considerations
Run in CI on every prompt, tool or model change (Lab 17.2). Agent Evaluation on the Agent Platform can run the same cases at scale.

## Cleanup
Delete `workspace/lab-12.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a freshness metric using Lab 5.2's superseded-policy cases.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
