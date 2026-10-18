# Lab 15.1 Public Authority Line and Transparency Record

**Book:** Chapter 15, section "15.4 The Transparency Record"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A Public Authority Line that keeps adverse decisions with delegated officers, statements of reasons, and a complete Transparency Record.

## Why This Matters
A citizen asks why their application was refused. 'The agent decided' is not an answer administrative law accepts.

## Enterprise Scenario
A state agency's permit pilot let the agent refuse an incomplete application.

## Learning Objectives
- Keep adverse outcomes with a human decision-maker
- Record reasons
- Publish a complete Transparency Record

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
chapter-15/lab-01-public-authority-and-transparency-record/
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
python shared/scripts/start-lab.py 15.1
cd workspace/lab-15.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read applications and the record.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Correct decisions and complete the record. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 15.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Synthetic applications only.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A batch job lets the agent refuse another application.
```
python ../../shared/scripts/start-lab.py 15.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `automated-adverse-decision`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: the officer re-decides and records reasons.
```
python ../../shared/scripts/start-lab.py 15.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[15.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (automated-adverse-decision) |
| After remediation | PASS |

## Evidence
`transparency-record.json`. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Requesting more information is not adverse in this model; check your own legal advice.

## Security Considerations
Automated decision transparency obligations under the Privacy Act are changing; verify current law.

## Enterprise Application
Legal signs the Public Authority Line.

## Production Considerations
Publish the Transparency Record in line with the current DTA policy for responsible use of AI in government; verify the version.

## Cleanup
Delete `workspace/lab-15.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a field for the AI system's accountable official.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
