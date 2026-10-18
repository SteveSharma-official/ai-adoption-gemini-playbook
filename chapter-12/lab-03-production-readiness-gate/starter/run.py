#!/usr/bin/env python3
"""Production Readiness Gate (Lab 12.3). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared"))
        break
from playbook.core import run  # noqa: E402
sys.exit(run("12.3", HERE))
