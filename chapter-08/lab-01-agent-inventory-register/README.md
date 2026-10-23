# Lab 8.1 Agent Inventory and Register

**Book:** Chapter 8, section "8.2 The Agent Inventory"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A reconciliation between the agents that exist (Gemini Enterprise app agents, Gems, Agent Platform agents) and the Agent Register, with owners and risk tiers.

## Why This Matters
You cannot govern an agent you cannot name. Most organisations discover agents they did not know they had.

## Enterprise Scenario
Kestrel finds a Customs Doc Checker in production built by someone who has since left.

## Learning Objectives
- Reconcile discovered agents with the register
- Reassign owners who have left
- Tier every agent by risk

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
chapter-08/lab-01-agent-inventory-register/
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
python shared/scripts/start-lab.py 8.1
cd workspace/lab-8.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `agents.json` and the register in `config.yaml`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Complete the register. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Where Agent Registry is available, export from it; the reconciliation logic is the same.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A leaver's 'Rates Bot' surfaces in a new scan.
```
python ../../shared/scripts/start-lab.py 8.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unregistered-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: register it with a new owner (then decide whether to retire it).
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unregistered-agent) |
| After remediation | PASS |

## Evidence
Reconciled register. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Leaver status comes from `users.csv`.

## Security Considerations
Unowned agents are rogue agents in waiting (OWASP ASI10).

## Enterprise Application
Register entry is a precondition for production access.

## Production Considerations
Run discovery weekly and alert on new agents.

## Cleanup
Delete `workspace/lab-8.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a 'retire by' date for agents with no use in 60 days.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
