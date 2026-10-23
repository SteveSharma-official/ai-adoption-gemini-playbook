# Lab 8.2 OWASP Agentic Threat Model

**Book:** Chapter 8, section "8.4 The Threat Model (OWASP Agentic)"
**Difficulty:** Level 4 (Secure)
**Effort:** 90 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A threat model that maps all ten OWASP Top 10 for Agentic Applications risks (ASI01 to ASI10, December 2025) to named controls and owners on Google.

## Why This Matters
A blank checklist is not a control plane. Mapping each risk to a control and an owner turns the threat model into something the CISO can test.

## Enterprise Scenario
Kestrel's threat model covers prompt injection, tool misuse and identity. Seven risks are blank.

## Learning Objectives
- Map every ASI risk to at least one control
- Use only controls that exist in the catalogue
- Assign owners

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
chapter-08/lab-02-owasp-agentic-threat-model/
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
python shared/scripts/start-lab.py 8.2
cd workspace/lab-8.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the control catalogue and threats.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Complete ASI04 to ASI10. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Control names in the catalogue use current Google capability names where they exist (Agent Gateway, Model Armor, Agent Sandbox). Verify against Appendix N before relying on them.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone removes the memory and context poisoning controls 'because the agent has no memory yet'.
```
python ../../shared/scripts/start-lab.py 8.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unmitigated-threat`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unmitigated-threat) |
| After remediation | PASS |

## Evidence
Threat-to-control map (also feeds Appendix G). Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Control names must match the catalogue exactly.

## Security Considerations
Re-run the model when you add memory, A2A or code execution.

## Enterprise Application
This map is the basis for red team scope (Lab 12.2).

## Production Considerations
Version the threat model with the agent.

## Cleanup
Delete `workspace/lab-8.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a control test for each control (see Lab 8.3).

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
