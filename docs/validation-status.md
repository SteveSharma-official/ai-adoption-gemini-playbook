# Validation Status

| Status | Meaning |
|---|---|
| DESIGN VALIDATED | The design was reviewed against the book and sources; nothing executed |
| STATICALLY VALIDATED | Files parse and lint; nothing executed |
| LOCALLY VALIDATED | Executed on a local machine with the stated versions and passed |
| CLOUD VALIDATION REQUIRED | Needs a real tenant or cloud service; not executed |
| EXECUTION VALIDATION REQUIRED | Not yet executed in the stated environment |

## Results on 2026-10-18
Environment: Linux container, Python 3.13.16, pytest 8.4.2, PyYAML 6.0.3. Synthetic data only.

Local proof sequence: **35 of 35 labs passed** (starter, solution, break it safely, prove the fix, evidence manifest).

| Lab | Local sequence | Cloud or Workspace steps | GitHub Actions |
|---|---|---|---|
| 0.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 0.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 1.1 | LOCALLY VALIDATED | CLOUD VALIDATION REQUIRED | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 1.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 2.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 2.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 3.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 4.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 5.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 5.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 6.1 | LOCALLY VALIDATED | CLOUD VALIDATION REQUIRED | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 6.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 6.3 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 7.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 7.2 | LOCALLY VALIDATED | CLOUD VALIDATION REQUIRED | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 8.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 8.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 8.3 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 9.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 10.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 11.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 12.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 12.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 12.3 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 13.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 14.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 15.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 15.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 16.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 16.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 17.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 17.2 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 17.3 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| 18.1 | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |
| Capstone | LOCALLY VALIDATED | Not applicable | PASSED (hosted runner, 18 and 20 Oct 2026) |

## GitHub Actions
The validate-labs workflow regenerates the datasets, checks they are unchanged, and runs every lab's proof sequence. It passed on GitHub's hosted ubuntu-latest runner with Python 3.13 on 18 October 2026 (push) and 20 October 2026 (weekly schedule), both on commit 9f95acb.
