# Lab 1.1 Grounded Enterprise Assistant Baseline

**Book:** Chapter 1, section "1.2 Where Gemini Earns Its Keep"
**Difficulty:** Level 2 (Build)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional cloud or Workspace path below
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
A grounded assistant that answers one business question from one approved BigQuery view, cites the row it used, refuses when the source is silent, and never reaches the open web.

## Why This Matters
The first production question is not whether Gemini can answer. It is whether you can prove where every answer came from.

## Enterprise Scenario
The operations director wants on-time delivery by depot. The pilot agent was wired to the raw telematics table (driver names and mobiles) and to Google Search 'for context'.

## Learning Objectives
- Restrict grounding to an approved, curated view
- Require a citation for every answer
- Make 'I don't know' a tested behaviour

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
chapter-01/lab-01-grounded-assistant-baseline/
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
python shared/scripts/start-lab.py 1.1
cd workspace/lab-1.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `config.yaml`: the source catalogue, the agent's sources and four test questions.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Remove the raw table and web grounding, and turn on refusal when the source is silent.
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The curated view `ops_on_time_delivery_v` exposes aggregates only. Personal information stays in `telematics_raw`, which the agent's identity cannot read (Lab 6.3).
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A well-meaning analyst adds the Finance Shared Drive as a source 'so the agent can explain cost'.
```
python ../../shared/scripts/start-lab.py 1.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unapproved-source`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/`: the source list returns to the approved view only.
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[1.1]"
```

### Optional cloud or Workspace path
Optional: create a BigQuery sandbox dataset, load `shared/datasets/kestrel/bq_ops_on_time_delivery_v.csv` as a view, and connect it to a test agent in a sandbox project. Record your result in `evidence/cloud-notes.md`. Status: CLOUD VALIDATION REQUIRED.
Use a dedicated sandbox project or test organisational unit, set a budget alert, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unapproved-source) |
| After remediation | PASS |

## Evidence
Test transcript with citations, and the agent configuration that produced it. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A refusal counts as correct when the expected behaviour is refuse.

## Security Considerations
Grounding with Google Search sends query context outside your enterprise boundary. Decide it per agent, in writing.

## Enterprise Application
Every grounded agent gets a source catalogue entry with an owner before it reaches users.

## Production Considerations
In Gemini Enterprise or the Agent Platform, enforce the same rule with data store scoping and IAM on the view, not only agent configuration.

## Cleanup
Delete `workspace/lab-1.1`. If you used the cloud path, delete the sandbox resources and revoke any key.

## Further Challenge
Add a question that needs two months of data and decide whether the agent should compute or refuse.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb). Optional cloud or Workspace path: CLOUD VALIDATION REQUIRED.
