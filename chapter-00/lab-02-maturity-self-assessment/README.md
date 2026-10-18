# Lab 0.2 AI Adoption Maturity Self-Assessment

**Book:** Chapter 0, section "0.3 The Method in One Page"
**Difficulty:** Level 1 (Explore)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A scored placement on the AI Adoption Maturity Model, where every level you claim is backed by named evidence.

## Why This Matters
Most organisations place themselves one level too high. The model only helps if the score is defensible to both the CIO and the CISO.

## Enterprise Scenario
Kestrel's steering committee slide says 'Level 3, Operational'. There is a pilot, an owner and a risk assessment. Nobody has written down the data boundary.

## Learning Objectives
- Map evidence to each maturity level
- Find the first missing piece of evidence
- Write the question that moves you up one level

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
chapter-00/lab-02-maturity-self-assessment/
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
python shared/scripts/start-lab.py 0.2
cd workspace/lab-0.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Edit `config.yaml`: list evidence against each key. Empty means not yet.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Correct the claimed level and add the missing evidence. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 0.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Evidence references point to documents; do not paste sensitive content into the file.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The steering committee raises the claim to Level 4 for the board paper.
```
python ../../shared/scripts/start-lab.py 0.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `maturity-overclaim`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again: the claim returns to what the evidence supports.
```
python ../../shared/scripts/start-lab.py 0.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[0.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (maturity-overclaim) |
| After remediation | PASS |

## Evidence
A signed maturity baseline the CIO and CISO can both sign. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A level is only met when every item below it is met.

## Security Considerations
Do not record secrets or personal information as evidence text.

## Enterprise Application
Re-score each quarter and report movement, not the score.

## Production Considerations
Store the assessment with the programme's governance records.

## Cleanup
Delete `workspace/lab-0.2`. No cloud resources are created by the local lab.

## Further Challenge
Add your own Level 3 evidence items for your organisation.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
