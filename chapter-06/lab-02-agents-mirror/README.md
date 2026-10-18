# Lab 6.2 The Agent's Mirror

**Book:** Chapter 6, section "6.2 The Agent's Mirror"
**Difficulty:** Level 4 (Secure)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A permission-aware retrieval simulation: a graduate asks the agent about salaries, and you see exactly what Gemini could surface for that person.

## Why This Matters
The agent is a mirror of each user's access. Testing as an administrator hides the problem; testing as the graduate shows it.

## Enterprise Scenario
A Kestrel finance graduate asks the assistant to 'summarise salary benchmarks'. The agent finds the 2019 salary review.

## Learning Objectives
- Test retrieval as a low-privilege user
- Trace the share that caused the exposure
- Prove the fix by re-running as the same user

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
chapter-06/lab-02-agents-mirror/
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
python shared/scripts/start-lab.py 6.2
cd workspace/lab-6.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
The query user is u012 (Graduate).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Remove the domain share on f001. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Run exposure tests with named personas, never with an admin account.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone adds the graduate to a broad finance readers group.
```
python ../../shared/scripts/start-lab.py 6.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `sensitive-retrieval`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: remove the membership and review the group's purpose.
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (sensitive-retrieval) |
| After remediation | PASS |

## Evidence
What the agent could surface, before and after. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Group membership changes are as dangerous as sharing changes.

## Security Considerations
Groups used for file access need owners and expiry.

## Enterprise Application
Build a persona test pack (graduate, contractor, executive assistant) and run it before each rollout wave.

## Production Considerations
Automate persona tests in a non-production Gemini Enterprise app.

## Cleanup
Delete `workspace/lab-6.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a contractor persona and test Board content.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
