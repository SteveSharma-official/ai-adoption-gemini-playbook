# Security Policy

## Synthetic data only
This repository must never contain real tenant exports, personal information, credentials, tokens or customer data. Kestrel Freight Group is fictional.

## Intentionally insecure material
Files under `lab-changes/` marked INTENTIONALLY INSECURE exist to be detected by the lab. Lab 0.1 contains a fake, non-working key-shaped string so the
secret check has something to find. Do not copy any of this material into a real environment.

## Cloud and Workspace paths
Labs 1.1, 6.1 and 7.2 include optional steps in Google Cloud or Google Workspace. Use a dedicated sandbox project or a test organisational unit you are
authorised to change, follow docs/cloud-sandbox-setup.md and docs/cost-and-cleanup.md, and keep keys in environment variables or Secret Manager.

## Reporting a vulnerability
Report suspected vulnerabilities in the lab code privately through GitHub's private vulnerability reporting for this repository.
Do not open a public issue for a vulnerability.
