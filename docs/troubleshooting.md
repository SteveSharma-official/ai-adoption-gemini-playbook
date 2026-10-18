# Troubleshooting

| Symptom | Fix |
|---|---|
| `PyYAML is required` | `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: playbook` | Run from inside the repository (run.py walks up to find `shared/playbook`) or set `PYTHONPATH=shared` |
| Dataset file not found | `python shared/scripts/generate_datasets.py` |
| Result differs from README | Apply overlays in order: solution, lab-changes, then the fix. Check `patches applied` in report.md |
| Workspace exists | Delete `workspace/lab-X.X` and start again |
| YAML `mapping values are not allowed` | Quote values that contain a colon |
