"""Every lab follows the same proof sequence:
starter -> expected status; + solution -> PASS; + lab-changes (break it safely) -> FAIL;
+ solution (or solution-after-break) -> PASS (prove the fix).
Run from the repository root: python -m pytest -q
"""
import json, os, shutil, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
LABS = sorted(p.parent for p in ROOT.glob("**/lab.json") if "workspace" not in p.parts)


def overlay(src: Path, dst: Path):
    if not src.exists():
        return
    for f in src.rglob("*"):
        if f.is_file() and f.name != "REMOVE.txt":
            t = dst / f.relative_to(src)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, t)
    rm = src / "REMOVE.txt"
    if rm.exists():
        for rel in rm.read_text().split():
            (dst / rel).unlink(missing_ok=True)


def run(work: Path) -> str:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "shared"))
    p = subprocess.run([sys.executable, "run.py"], cwd=work, env=env, capture_output=True, text=True, timeout=120)
    assert p.returncode in (0, 1), p.stderr
    status = json.loads((work / "evidence" / "result.json").read_text())["status"]
    assert (status == "PASS") == (p.returncode == 0)
    return status


@pytest.mark.parametrize("lab", LABS, ids=[json.loads((l / "lab.json").read_text())["id"] for l in LABS])
def test_lab_sequence(lab, tmp_path):
    meta = json.loads((lab / "lab.json").read_text())
    work = tmp_path / "work"
    shutil.copytree(lab / "starter", work)
    assert run(work) == meta["starter_status"], "starter"
    overlay(lab / "solution", work)
    assert run(work) == "PASS", "solution"
    overlay(lab / "lab-changes", work)
    assert run(work) == "FAIL", "break it safely"
    overlay(lab / ("solution-after-break" if meta["has_solution_after_break"] else "solution"), work)
    assert run(work) == "PASS", "prove the fix"
    manifest = json.loads((work / "evidence" / "manifest.json").read_text())
    assert manifest["status"] == "PASS" and "result.json" in manifest["sha256"]
