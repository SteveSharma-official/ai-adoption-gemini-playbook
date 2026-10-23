# Lab 2.1 Enterprise AI Portfolio Map

**Book:** Chapter 2, section "2.3 The Enterprise AI Portfolio Map"
**Difficulty:** Level 2 (Build)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A validated AI Portfolio Map: every workload placed on a platform by where its data lives, with an identity boundary and a written justification for every exception.

## Why This Matters
No enterprise runs one AI platform. Data gravity is the strongest placement signal, but connectors make exceptions legitimate if they are justified and governed.

## Enterprise Scenario
Kestrel runs Workspace and BigQuery, but its acquired Customs Brokerage division runs Microsoft 365. Analysts are using personal ChatGPT for route analysis.

## Learning Objectives
- Place workloads by data location
- Record a connector justification for cross-estate placements
- Exclude unsanctioned platforms from enterprise data

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
chapter-02/lab-01-ai-portfolio-map/
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
python shared/scripts/start-lab.py 2.1
cd workspace/lab-2.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the platforms and workloads in `config.yaml`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Re-place the workloads and justify the one deliberate exception. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Each platform must have an identity boundary. A platform with none cannot hold enterprise data.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Finance adds a payroll forecast on personal ChatGPT.
```
python ../../shared/scripts/start-lab.py 2.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unsanctioned-platform`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/`: the workload list returns to the ratified map.
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[2.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unsanctioned-platform) |
| After remediation | PASS |

## Evidence
Placement table and a Mermaid portfolio diagram (`portfolio-map.mmd`). Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A connector exception needs a non-empty justification.

## Security Considerations
Cross-estate connectors duplicate index and permission surfaces; review them like any integration.

## Enterprise Application
The map becomes the architecture board's reference for every new AI request.

## Production Considerations
Review the map quarterly and after any acquisition.

## Cleanup
Delete `workspace/lab-2.1`. No cloud resources are created by the local lab.

## Further Challenge
Add an open-weight model hosted in your own project and decide what data it may hold.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
