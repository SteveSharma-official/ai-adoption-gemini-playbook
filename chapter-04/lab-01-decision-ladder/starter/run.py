#!/usr/bin/env python3
"""The Decision Ladder (Lab 4.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared"))
        break
from playbook.core import run  # noqa: E402
sys.exit(run("4.1", HERE))
