"""Core helpers for Book 2 labs: config with overlay patches, dataset access, and the lab runner.

Each lab folder holds `config.yaml`. Overlays (solution, lab-changes, solution-after-break) add numbered patch files
(`patch-10-*.yaml`, `patch-20-*.yaml`, `patch-30-*.yaml`). Patches are deep-merged in name order, so the proof sequence
is readable: you can open each patch and see exactly what the fix or the break changed.

Merge rules: dicts merge recursively; a key ending in `__append` appends to the list of the same name;
a key ending in `__remove` removes list items whose `id` (or `name`, or the item itself) matches; other values replace.
"""
from __future__ import annotations
import copy, json
from pathlib import Path
from .common import Result, finish, load, md_table, DATASETS  # noqa: F401


def _key(item):
    if isinstance(item, dict):
        return item.get("id", item.get("name"))
    return item


def merge(base, patch):
    out = copy.deepcopy(base)
    for k, v in (patch or {}).items():
        if k.endswith("__append"):
            out.setdefault(k[:-8], []).extend(copy.deepcopy(v))
        elif k.endswith("__remove"):
            drop = set(v)
            out[k[:-8]] = [i for i in out.get(k[:-8], []) if _key(i) not in drop]
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def config(lab_dir) -> dict:
    lab_dir = Path(lab_dir)
    cfg = load(lab_dir / "config.yaml") or {}
    patches = sorted(lab_dir.glob("patch-*.yaml"))
    for p in patches:
        cfg = merge(cfg, load(p))
    cfg["_applied"] = [p.name for p in patches]
    return cfg


def ds(name):
    """Load a file from the Kestrel Freight Group synthetic dataset."""
    return load(DATASETS / name)


def users():
    return {u["user_id"]: u for u in ds("users.csv")}


def groups():
    g = {}
    for r in ds("group_members.csv"):
        g.setdefault(r["group"], set()).add(r["user_id"])
    return g


def report(title, result: Result, sections: list[tuple[str, str]]) -> str:
    """A consistent evidence report: what ran, the verdict, findings, then lab-specific sections."""
    status = "PASS" if result.passed else "FAIL"
    md = [f"# Lab {result.lab_id} {title}", "", f"**Status:** {status}", ""]
    if result.data.get("applied"):
        md += [f"**Patches applied:** {', '.join(result.data['applied'])}", ""]
    md += ["## Findings", md_table(result.findings, ["rule", "blocking", "message"])]
    for h, body in sections:
        md += [f"## {h}", body, ""]
    md += ["---", "Synthetic data only (Kestrel Freight Group is fictional). Evidence hashes are in manifest.json."]
    return "\n".join(md)


def run(lab_id: str, lab_dir) -> int:
    from . import labs_a, labs_b
    fn = labs_a.REGISTRY.get(lab_id) or labs_b.REGISTRY.get(lab_id)
    if fn is None:
        raise SystemExit(f"Unknown lab {lab_id}")
    cfg = config(lab_dir)
    result, title, sections, extra = fn(cfg, Path(lab_dir))
    result.data["applied"] = cfg["_applied"]
    return finish(result, Path(lab_dir) / "evidence", report(title, result, sections), extra)


def new(lab_id, title):
    return Result(lab_id, title)


def dump(obj) -> str:
    return "```json\n" + json.dumps(obj, indent=2, default=str) + "\n```"
