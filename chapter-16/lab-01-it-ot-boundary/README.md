# Lab 16.1 IT and OT Boundary

**Book:** Chapter 16, section "16.1 The OT Boundary"
**Difficulty:** Level 4 (Secure)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A Purdue-model review of an engineering agent's tools: read SOPs and replicated telemetry from the DMZ, never touch control systems.

## Why This Matters
The maintenance manual is 4,000 pages and the technician has nine minutes. The agent can help, but only from the right side of the boundary.

## Enterprise Scenario
Kestrel's fleet engineering agent reads live SCADA tags at the Brisbane depot.

## Learning Objectives
- Classify tools by Purdue zone
- Move reads to a DMZ historian replica
- Block any write path to OT

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
chapter-16/lab-01-it-ot-boundary/
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
python shared/scripts/start-lab.py 16.1
cd workspace/lab-16.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the tools.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Replace the direct read. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 16.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Map to ISA/IEC 62443 zones and conduits.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer adds a PLC set-point tool for a demo.
```
python ../../shared/scripts/start-lab.py 16.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `ot-write-path`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 16.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[16.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (ot-write-path) |
| After remediation | PASS |

## Evidence
Tool zone table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Read access to L2 is also blocking in this model.

## Security Considerations
No AI agent has a write path into OT, at any approval level.

## Enterprise Application
The OT owner signs the tool list.

## Production Considerations
Enforce at the firewall, not only in agent configuration.

## Cleanup
Delete `workspace/lab-16.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a safety-instrumented system zone.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
