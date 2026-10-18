"""Common helpers: loading inputs, writing evidence, and a consistent result shape."""
from __future__ import annotations
import csv, hashlib, json, os, sys, datetime as dt
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install -r requirements.txt")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASETS = REPO_ROOT / "shared" / "datasets" / "kestrel"


def load(path):
    path = Path(path)
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix == ".jsonl":
        return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    return path.read_text(encoding="utf-8")


def parse_date(s):
    return dt.date.fromisoformat(str(s)[:10]) if s else None


def parse_ts(s):
    return dt.datetime.fromisoformat(str(s))


class Result:
    """PASS/FAIL outcome with findings. A lab fails when any finding is blocking."""

    def __init__(self, lab_id: str, title: str):
        self.lab_id, self.title = lab_id, title
        self.findings: list[dict] = []
        self.data: dict = {}
        self.notes: list[str] = []

    def find(self, rule: str, message: str, blocking: bool = True, **extra):
        self.findings.append({"rule": rule, "message": message, "blocking": blocking, **extra})

    @property
    def passed(self) -> bool:
        return not any(f["blocking"] for f in self.findings)

    def to_dict(self):
        return {"lab": self.lab_id, "title": self.title, "status": "PASS" if self.passed else "FAIL",
                "blocking_findings": sum(f["blocking"] for f in self.findings),
                "findings": self.findings, "data": self.data, "notes": self.notes}


def write_evidence(result: Result, out_dir, report_md: str | None = None, extra_files: dict | None = None):
    """Write result.json, report.md and a SHA-256 manifest so the evidence can be checked later."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = {"result.json": json.dumps(result.to_dict(), indent=2, default=str)}
    if report_md:
        files["report.md"] = report_md
    for k, v in (extra_files or {}).items():
        files[k] = v
    manifest = {}
    for name, content in files.items():
        p = out / name
        p.write_text(content, encoding="utf-8")
        manifest[name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
    (out / "manifest.json").write_text(json.dumps({
        "lab": result.lab_id, "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS" if result.passed else "FAIL", "sha256": manifest}, indent=2), encoding="utf-8")
    return out


def finish(result: Result, out_dir, report_md: str | None = None, extra_files: dict | None = None) -> int:
    write_evidence(result, out_dir, report_md, extra_files)
    status = "PASS" if result.passed else "FAIL"
    print(f"[{result.lab_id}] {result.title}: {status}")
    for f in result.findings:
        flag = "BLOCK" if f["blocking"] else "note "
        print(f"  {flag} {f['rule']}: {f['message']}")
    print(f"  evidence: {Path(out_dir).resolve()}")
    return 0 if result.passed else 1


def md_table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "_none_\n"
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")).replace("|", "/") for c in cols) + " |")
    return "\n".join(out) + "\n"
