#!/usr/bin/env python3
"""Start a lab or apply one of its overlays.

  python shared/scripts/start-lab.py 6.1                  copy starter/ into workspace/lab-6.1
  python shared/scripts/start-lab.py 6.1 --apply solution  overlay solution/ (or lab-changes, solution-after-break)
"""
import argparse, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def find(lab_id):
    for p in ROOT.glob("**/lab.json"):
        if "workspace" in p.parts:
            continue
        if json.loads(p.read_text())["id"].lower() == lab_id.lower():
            return p.parent
    sys.exit(f"No lab with id {lab_id}. See README.md for the lab index.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lab")
    ap.add_argument("--apply", choices=["solution", "lab-changes", "solution-after-break"])
    a = ap.parse_args()
    lab = find(a.lab)
    ws = ROOT / "workspace" / f"lab-{a.lab}"
    if not a.apply:
        if ws.exists():
            sys.exit(f"{ws} exists. Delete it to start again.")
        shutil.copytree(lab / "starter", ws)
        print(f"Workspace ready: {ws}")
        return
    src = lab / a.apply
    if not src.exists():
        sys.exit(f"Lab {a.lab} has no {a.apply}/ folder.")
    for f in src.rglob("*"):
        if f.is_file() and f.name != "REMOVE.txt":
            t = ws / f.relative_to(src); t.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, t)
    rm = src / "REMOVE.txt"
    if rm.exists():
        for rel in rm.read_text().split():
            (ws / rel).unlink(missing_ok=True)
            print(f"removed {rel}")
    print(f"Applied {a.apply} to {ws}")


if __name__ == "__main__":
    main()
