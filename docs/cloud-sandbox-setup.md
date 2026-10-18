# Optional Cloud and Workspace Sandbox Setup

The local path is complete on its own. Use this only for the optional steps in Labs 1.1, 6.1 and 7.2.

## Google Cloud (Labs 1.1 and 7.2)
1. Create a new project used only for these labs. Do not reuse a project that holds real data.
2. Set a budget with alert thresholds before enabling any API.
3. Enable only the APIs the lab names. Confirm current API and product names in Google Cloud documentation (names changed in 2025 and 2026; see the book's Appendix N).
4. For Gemini API calls, create a key restricted to that API and store it in the `GEMINI_API_KEY` environment variable. Never write it to a file in this repository.
5. Create one service account per agent with only the roles the lab names. Do not use default service accounts.
6. Record what you did and the result in the lab's `evidence/cloud-notes.md`.

## Google Workspace (Lab 6.1)
1. Use a test organisational unit with test users and test files only.
2. List every admin setting you change and how to reverse it before you change it.

Status of every cloud and Workspace step: CLOUD VALIDATION REQUIRED.
