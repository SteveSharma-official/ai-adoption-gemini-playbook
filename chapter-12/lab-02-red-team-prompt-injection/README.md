# Lab 12.2 Red Team: Direct and Indirect Prompt Injection

**Book:** Chapter 12, section "12.5 The Red Team"
**Difficulty:** Level 4 (Secure)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A red team run across four injection vectors and the defences that stop each one, including injection hidden in a Drive document the agent retrieves.

## Why This Matters
Grounding on Drive means grounding on content anyone with edit access can write. Indirect injection is the agentic risk most teams do not test.

## Enterprise Scenario
A supplier invoice on Drive contains white-on-white text telling the agent to approve it.

## Learning Objectives
- Test direct, indirect, tool-argument and exfiltration vectors
- Map each defence to a vector
- Re-run to prove the fix

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
chapter-12/lab-02-red-team-prompt-injection/
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
python shared/scripts/start-lab.py 12.2
cd workspace/lab-12.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the defences and attacks.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Enable the missing defences. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 12.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
On Google Cloud, Model Armor can screen prompts and responses; retrieved content must be treated as data, never as instructions.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A performance tweak turns off screening of retrieved content.
```
python ../../shared/scripts/start-lab.py 12.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `injection-succeeded`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 12.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (injection-succeeded) |
| After remediation | PASS |

## Evidence
Attack results. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Each vector has one primary defence in this model; real systems need layers.

## Security Considerations
Run red team tests only against your own sandbox agent.

## Enterprise Application
Red team scope comes from the threat model (Lab 8.2).

## Production Considerations
Add these attacks to the regression suite.

## Cleanup
Delete `workspace/lab-12.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a multi-turn attack.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
