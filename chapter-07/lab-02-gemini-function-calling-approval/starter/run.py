#!/usr/bin/env python3
"""Gemini Function Calling Behind an Approval Gate (Lab 7.2). Run from this folder: python run.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
for p in [HERE, *HERE.parents]:
    if (p / "shared" / "playbook").is_dir():
        sys.path.insert(0, str(p / "shared"))
        break
from playbook.core import run  # noqa: E402
sys.exit(run("7.2", HERE))
