# Lab 0.1 Quick Start and Lab Safety Check

**Book:** Introduction, section "How the book, templates and labs work together"
**Difficulty:** Level 1 (Explore)
**Effort:** 20 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A working lab environment and your first evidence pack, plus a safety check that refuses to run against production or with a key pasted into a file.

## Why This Matters
Every later lab produces evidence. If the first habit you learn is pasting an API key into a config file and pointing it at production, the labs teach the opposite of the book.

## Enterprise Scenario
Kestrel Freight Group's architect wants to try the labs on the production Google Cloud project 'just to see real numbers'. This lab is the polite no.

## Learning Objectives
- Run a lab and read its evidence pack (result.json, report.md, manifest.json)
- Recognise the local, cloud and Workspace execution paths
- Detect a credential committed to a config file

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
chapter-00/lab-01-quick-start/
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
python shared/scripts/start-lab.py 0.1
cd workspace/lab-0.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Open `config.yaml`. The target is `local` and no key is configured.
```
python run.py
```
Expected: `PASS`. The starter is the compliant baseline.

### Step 3. Build
Nothing to build: the starter is the compliant baseline. Run it and confirm PASS.
```
python ../../shared/scripts/start-lab.py 0.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Read `SECURITY.md`. Keys for the optional cloud path live in an environment variable (`GEMINI_API_KEY`) or Secret Manager, never in a file.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
`lab-changes/` points the lab at `kestrel-prod` and pastes a (fake, non-working) API key into a patch file.
```
python ../../shared/scripts/start-lab.py 0.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `secret-in-config`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/`: it removes the unsafe patch. In real life you would also revoke the exposed key immediately.
```
python ../../shared/scripts/start-lab.py 0.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[0.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | PASS |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (secret-in-config) |
| After remediation | PASS |

## Evidence
The evidence pack format used by every lab. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Dataset missing: run `python shared/scripts/generate_datasets.py`.

## Security Considerations
Treat any key that touched a file or a commit as compromised: revoke it, do not just delete the line.

## Enterprise Application
Add a secret scanner (for example a pre-commit hook) to every repository your AI team uses.

## Production Considerations
Use Workload Identity Federation or attached service accounts in place of API keys wherever the platform allows.

## Cleanup
Delete `workspace/lab-0.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a pre-commit hook that runs this check before every commit.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
