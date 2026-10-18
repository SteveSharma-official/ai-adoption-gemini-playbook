# Lab 5.1 Reference Architecture as Code

**Book:** Chapter 5, section "5.4 Designing the Reference Architecture"
**Difficulty:** Level 2 (Build)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
The Kestrel reference architecture as a YAML file that a script validates and turns into a Mermaid diagram, covering five layers, every agent's identity, and what stays locked.

## Why This Matters
Organisations buy Gemini Enterprise as an architecture and use it as a browser extension. Drawing the layers forces the identity and logging questions early.

## Enterprise Scenario
The CIO opens the console and sees model APIs, the Agent Platform, Workspace features and BigQuery connections. Nobody can say which identity the Procurement Agent runs as.

## Learning Objectives
- Describe the three Gemini layers plus data and security
- Give every agent a dedicated identity, owner and log destination
- Record what stays locked and why

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
chapter-05/lab-01-reference-architecture-as-code/
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
python shared/scripts/start-lab.py 5.1
cd workspace/lab-5.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `config.yaml`. The security layer is empty; one agent runs as the Compute Engine default service account.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fill the security layer and give the Procurement Agent its own identity.
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Default service accounts often hold broad project roles. An agent never runs as one.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Sales adds a Quote Agent on the App Engine default identity, with Google Search grounding.
```
python ../../shared/scripts/start-lab.py 5.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `default-service-account`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: a dedicated identity and no web grounding.
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (default-service-account) |
| After remediation | PASS |

## Evidence
`reference-architecture.mmd` (editable diagram source) and the validation report. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Every layer needs at least one component, even if it is locked.

## Security Considerations
Product names change; Appendix N tracks current names. The pattern does not.

## Enterprise Application
The CISO signs this file, not a slide.

## Production Considerations
Keep the YAML in the platform team's repository and validate it in CI.

## Cleanup
Delete `workspace/lab-5.1`. No cloud resources are created by the local lab.

## Further Challenge
Add an MCP server as a tool source and decide which layer and identity it belongs to.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: EXECUTION VALIDATION REQUIRED on a hosted runner.
