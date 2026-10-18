# Lab 4.1 The Decision Ladder

**Book:** Chapter 4, section "4.2 The Decision Ladder"
**Difficulty:** Level 2 (Build)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A Decision Ladder record for each workload: Buy, Configure, Integrate, Build or Host, with the minimum rung computed from the workload and any higher choice justified.

## Why This Matters
Three teams, three tools, one requirement. Choosing the rung before the tool stops six months of overlapping builds.

## Enterprise Scenario
Kestrel engineering wants to build a custom meeting summariser on the Agent Platform. Gemini in Meet already does it.

## Learning Objectives
- Compute the minimum rung from workload facts
- Catch over-engineering and under-scoping
- Record justification for higher rungs

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
chapter-04/lab-01-decision-ladder/
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
python shared/scripts/start-lab.py 4.1
cd workspace/lab-4.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Workload attributes: workflow_specific, acts_on_enterprise_systems, no_platform_fit, sovereign_hosting_required.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Correct the rungs. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Each rung up adds an identity, a data path and an owner. Count them before you climb.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A team proposes a custom-built policy FAQ agent.
```
python ../../shared/scripts/start-lab.py 4.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `over-engineered`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: the FAQ moves to Buy (Gemini Enterprise search over the policy folder).
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[4.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (over-engineered) |
| After remediation | PASS |

## Evidence
Rung decisions with rationale. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A higher rung is allowed with a written justification.

## Security Considerations
Higher rungs need Lab 6.3 identity controls before build.

## Enterprise Application
Make the ladder an architecture board entry criterion.

## Production Considerations
Re-test the rung when Google ships a capability that moves a workload down.

## Cleanup
Delete `workspace/lab-4.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a workload that genuinely needs Host and explain why.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
