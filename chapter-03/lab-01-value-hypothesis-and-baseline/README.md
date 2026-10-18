# Lab 3.1 Value Hypothesis and Baseline

**Book:** Chapter 3, section "3.3 Writing the Value Hypothesis"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 30 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A one-page value hypothesis tied to a business number, a measured baseline and a system of record.

## Why This Matters
Usage proves people like the tool. It does not prove value. The CFO asks which prompt changed a business number.

## Enterprise Scenario
Kestrel's draft success measure for the claims pilot is prompts per user per week.

## Learning Objectives
- Separate activity metrics from business metrics
- Anchor the target to the measured baseline from Lab 1.2
- Name where the number will come from

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
chapter-03/lab-01-value-hypothesis-and-baseline/
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
python shared/scripts/start-lab.py 3.1
cd workspace/lab-3.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the hypothesis in `config.yaml`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Rewrite the metric as a business number. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Measurement data stays in the system of record; the hypothesis references it.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Marketing changes the success measure to adoption rate for the internal newsletter.
```
python ../../shared/scripts/start-lab.py 3.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `vanity-metric`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[3.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (vanity-metric) |
| After remediation | PASS |

## Evidence
The signed hypothesis. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Words like prompts, usage and active users trigger the vanity check.

## Security Considerations
Not applicable beyond normal document handling.

## Enterprise Application
Adoption metrics can sit beside the value metric, never in place of it.

## Production Considerations
Report the value metric monthly through the Executive Dashboard (Lab 18.1).

## Cleanup
Delete `workspace/lab-3.1`. No cloud resources are created by the local lab.

## Further Challenge
Write a second hypothesis for a quality metric (error rate) rather than speed.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
