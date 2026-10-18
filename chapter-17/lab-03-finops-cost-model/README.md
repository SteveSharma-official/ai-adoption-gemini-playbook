# Lab 17.3 FinOps Cost Model

**Book:** Chapter 17, section "17.4 The FinOps Angle"
**Difficulty:** Level 7 (Deploy)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
Unit economics for each agent (cost per outcome against value per outcome), budget guardrails and licence utilisation.

## Why This Matters
The first agent paid for itself. Consumption-priced agents can quietly stop doing so. Cost per outcome is the number that survives a budget review.

## Enterprise Scenario
Kestrel's quote drafting agent costs more per month than the value it creates.

## Learning Objectives
- Compute cost per outcome
- Set budget alerts and a cap
- Track idle licences

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
chapter-17/lab-03-finops-cost-model/
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
python shared/scripts/start-lab.py 17.3
cd workspace/lab-17.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read agents and guardrails. All prices are illustrative, not Google list prices.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add guardrails and fix the quote agent's economics. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 17.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Budget caps can stop a runaway agent loop; treat them as a safety control too.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Budget alerts are deleted during a project migration.
```
python ../../shared/scripts/start-lab.py 17.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-budget-guardrail`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 17.3 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-budget-guardrail) |
| After remediation | PASS |

## Evidence
Unit economics table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Idle licences are a note, not a failure.

## Security Considerations
Not applicable beyond normal billing access control.

## Enterprise Application
Finance owns the value figures; the platform team owns cost.

## Production Considerations
Use billing export to BigQuery for actual costs.

## Cleanup
Delete `workspace/lab-17.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a per-user daily call cap.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
