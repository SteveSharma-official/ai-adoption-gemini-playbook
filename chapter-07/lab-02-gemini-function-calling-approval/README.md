# Lab 7.2 Gemini Function Calling Behind an Approval Gate

**Book:** Chapter 7, section "7.3 Tool Use and API Permissions"
**Difficulty:** Level 4 (Secure)
**Effort:** 60 minutes (90 with cloud path)
**Execution paths:** Local (default, synthetic data, no API key); optional cloud or Workspace path below
**API key needed:** No (local path); the optional cloud path uses `GEMINI_API_KEY` from the environment
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A function-calling trace review: every consequential function is declared with an approval requirement, allowlisted, argument-bounded and executed only with an approval token.

## Why This Matters
With function calling the model proposes the action and your code executes it. The approval gate lives in your code, not in the prompt.

## Enterprise Scenario
The Procurement Agent's function declarations let the model call create_purchase_order with no approval step.

## Learning Objectives
- Declare consequential functions with approval requirements
- Hold execution until an approval token exists
- Never declare functions the agent must not use

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
chapter-07/lab-02-gemini-function-calling-approval/
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
python shared/scripts/start-lab.py 7.2
cd workspace/lab-7.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the tool declarations and the call trace.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Mark the PO function as requiring approval and update the trace. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
If the model can see a function declaration, assume it will eventually call it. Do not declare human-only functions.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer declares execute_payment 'for a demo'.
```
python ../../shared/scripts/start-lab.py 7.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `consequential-tool-exposed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again: the declaration is removed.
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.2]"
```

### Optional cloud or Workspace path
Optional: in a sandbox project, call the Gemini API with these function declarations using a key from `GEMINI_API_KEY`, write your executor so that it refuses `create_purchase_order` without a token, and save the trace. CLOUD VALIDATION REQUIRED.
Use a dedicated sandbox project or test organisational unit, set a budget alert, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (consequential-tool-exposed) |
| After remediation | PASS |

## Evidence
Annotated call trace. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Held calls are not findings; executed calls without tokens are.

## Security Considerations
Never pass approval tokens through model output; your gateway issues and checks them.

## Enterprise Application
Same matrix as Lab 7.1, now at the code level.

## Production Considerations
Log the function name, arguments, approval token and approver for every consequential call.

## Cleanup
Delete `workspace/lab-7.2`. If you used the cloud path, delete the sandbox resources and revoke any key.

## Further Challenge
Add argument validation for supplier IDs against an allowlist.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner. Optional cloud or Workspace path: CLOUD VALIDATION REQUIRED.
