# Lab 6.3 Agent Identity and IAM Audit

**Book:** Chapter 6, section "6.4 Scoped Identities for Agents"
**Difficulty:** Level 4 (Secure)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Kestrel Freight Group is fictional; domain kestrel.example)

## What You Will Build
An audit of agent service accounts: basic roles, access to raw personal data, stale user-managed keys and owners who have left, followed by a least-privilege fix.

## Why This Matters
An agent's blast radius is its identity's permissions. 'Editor because it was quicker' is the most common finding in agent reviews.

## Enterprise Scenario
The HR Answers Agent runs with Editor on the project, and its owner left in August. The Freight Ops Assistant can read raw telematics.

## Learning Objectives
- Find basic roles on agent identities
- Remove access to restricted datasets
- Retire user-managed keys and reassign owners

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
chapter-06/lab-03-agent-identity-audit/
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
python shared/scripts/start-lab.py 6.3
cd workspace/lab-6.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `iam_policy.json` and `service_accounts.json` in the dataset.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Remove and replace bindings, keys and owners. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Prefer attached service accounts or Workload Identity Federation to keys. Where Agent Identity is available, map it to the same least-privilege policy.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer grants roles/editor to the Procurement Agent to fix a permission error.
```
python ../../shared/scripts/start-lab.py 6.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `basic-role-on-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: the binding is removed again.
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (basic-role-on-agent) |
| After remediation | PASS |

## Evidence
Effective bindings after remediation. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The Compute Engine default service account is flagged even with no agent attached.

## Security Considerations
Role names are examples; confirm the predefined roles your agent surface needs in current Google documentation.

## Enterprise Application
Every agent identity has an owner in the Agent Register (Lab 8.1).

## Production Considerations
Use IAM Recommender and organisation policies to block key creation.

## Cleanup
Delete `workspace/lab-6.3`. No cloud resources are created by the local lab.

## Further Challenge
Write the organisation policy constraint that would have prevented the break.

---
Validation status: LOCALLY VALIDATED: the full sequence (starter, solution, break it safely, prove the fix) passed on 2026-10-18 with Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3, using synthetic data only. GitHub Actions workflow: PASSED on a hosted runner (validate-labs, ubuntu-latest, Python 3.13: push run 18 October 2026 and scheduled run 20 October 2026, commit 9f95acb).
