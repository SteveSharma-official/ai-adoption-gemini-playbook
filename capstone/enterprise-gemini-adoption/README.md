# Enterprise Gemini Adoption Capstone

**Book:** "Chapters 1 to 18"
**Difficulty:** Level 8 (Scale)
**Effort:** 4 to 6 hours
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
An end-to-end adoption case for Kestrel's claims agent: baseline, placement, exposure, identity, authority, evaluation, red team, logging, value and operating model, ending in a Day 90 verdict.

## Why This Matters
This is the journey from AI experiment to governed enterprise capability, in one file you can defend to a board.

## Enterprise Scenario
Kestrel's claims agent pilot reaches Day 90. The steering committee wants a production decision.

## Learning Objectives
- Bring the evidence from earlier labs into one case
- Pass every production gate
- Produce a defensible Go or Not ready verdict

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
capstone/enterprise-gemini-adoption/
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
python shared/scripts/start-lab.py Capstone
cd workspace/lab-Capstone
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `config.yaml`: each field is evidence produced by an earlier lab.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Work through the labs referenced in the README and update the case. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py Capstone --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The capstone re-checks the security gates from Chapters 6 to 8.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A late change lets the agent pay claims directly.
```
python ../../shared/scripts/start-lab.py Capstone --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `capstone-gate`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py Capstone --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[Capstone]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (capstone-gate) |
| After remediation | PASS |

## Evidence
Gate table and verdict. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Every gate must pass for Go.

## Security Considerations
Synthetic data only.

## Enterprise Application
Use this structure for your own Day 90 pack.

## Production Considerations
Replace each field with a link to real evidence.

## Cleanup
Delete `workspace/lab-Capstone`. No cloud resources are created by the local lab.

## Further Challenge
Run the capstone for a second process from Lab 9.1.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
