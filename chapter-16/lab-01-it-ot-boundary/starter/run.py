#!/usr/bin/env python3
"""IT and OT Boundary (Lab 16.1). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared"))
        break
from playbook.core import run  # noqa: E402
sys.exit(run("16.1", HERE))
