# Lab 16.2 Retail Pricing and Refund Rules

**Book:** Chapter 16, section "16.3 The Checkout and the Consumer"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A rules engine that lets the customer agent refund small amounts, proposes larger refunds and all price changes to people, and routes vulnerable customers to a specialist team.

## Why This Matters
Commercial decisions and consumer law obligations belong in deterministic rules with owners, not in a model's judgement.

## Enterprise Scenario
Kestrel's parcel service agent refunded 640 dollars and changed a price on request.

## Learning Objectives
- Set an auto-execution limit
- Reserve price changes for people
- Route vulnerable customers

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
chapter-16/lab-02-retail-pricing-and-refund-rules/
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
python shared/scripts/start-lab.py 16.2
cd workspace/lab-16.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read rules and requests.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Restrict the agent's actions. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 16.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Price and refund tools sit behind the gateway from Lab 7.1.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Price changes are re-enabled for a 'dynamic offers' trial.
```
python ../../shared/scripts/start-lab.py 16.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `commercial-decision-by-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 16.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[16.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (commercial-decision-by-agent) |
| After remediation | PASS |

## Evidence
Outcomes table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Vulnerable routing overrides every other rule.

## Security Considerations
Australian Consumer Law obligations apply to what the agent tells customers; verify with legal.

## Enterprise Application
Commercial owners sign the limits.

## Production Considerations
Review limits monthly against refund data.

## Cleanup
Delete `workspace/lab-16.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a daily cap on total agent refunds.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
