# Cost and Cleanup

Local labs: no cost and no cloud resources. Delete `workspace/` when finished.

Optional cloud path: Gemini API calls, BigQuery queries and Agent Platform resources are billed by Google. Prices change; check current pricing before you start
and keep a budget alert on the sandbox project. After the lab:
1. Delete any test agents, data stores and BigQuery datasets you created.
2. Revoke and delete API keys and service account keys.
3. Delete the sandbox project if it was created only for the labs.
4. Confirm in Billing that consumption has stopped.

Optional Workspace path: reverse every setting you changed, remove test shares and delete test files.
