"""Lab engines for Parts I and II (Chapters 0 to 8).

Every function takes the merged lab config and the lab folder, and returns
(Result, title, report sections, extra evidence files or None).
The checks model the decisions the book teaches. They do not call Google APIs; cloud steps are optional and documented in each README.
"""
from __future__ import annotations
import re, statistics, datetime as dt
from .core import new, ds, users, groups, md_table, dump
from .common import parse_ts, parse_date

SECRET = re.compile(r"(AIza[0-9A-Za-z_\-]{35}|-----BEGIN (RSA )?PRIVATE KEY-----|\"private_key\":)")
TODAY = dt.date(2026, 10, 18)


# ---------- Chapter 0 ----------
def quick_start(cfg, lab):
    r = new("0.1", "Quick Start and Lab Safety Check")
    env = cfg.get("environment", {})
    files = [p for p in lab.rglob("*") if p.is_file() and "evidence" not in p.parts]
    for p in files:
        if SECRET.search(p.read_text(encoding="utf-8", errors="ignore")):
            r.find("secret-in-config", f"{p.name} contains something that looks like a credential. Use an environment variable or Secret Manager.")
    if env.get("target") not in ("local", "sandbox"):
        r.find("non-sandbox-target", f"target is '{env.get('target')}'. Labs run locally or in an isolated sandbox project only.")
    if not (ds("users.csv")):
        r.find("dataset-missing", "Run python shared/scripts/generate_datasets.py")
    r.data["environment"] = env
    return r, "Quick Start and Lab Safety Check", [("Environment", dump(env))], None


LEVELS = {2: ["named_use_case", "business_owner", "risk_assessment", "data_boundary"],
          3: ["production_kpis", "identity_controls", "logging", "evaluation", "escalation_path"],
          4: ["shared_platform", "central_governance", "enterprise_observability", "reusable_agents"],
          5: ["cross_platform_orchestration", "adaptive_governance"]}


def maturity(cfg, lab):
    r = new("0.2", "AI Adoption Maturity Self-Assessment")
    have = {k for k, v in (cfg.get("evidence") or {}).items() if v}
    level = 1
    gaps = []
    for lv in sorted(LEVELS):
        missing = [k for k in LEVELS[lv] if k not in have]
        if missing:
            gaps.append({"level": lv, "missing": ", ".join(missing)})
            break
        level = lv
    claimed = int(cfg.get("claimed_level", 1))
    r.data.update(claimed=claimed, evidenced=level)
    if claimed > level:
        r.find("maturity-overclaim", f"Claimed level {claimed} but evidence supports level {level}. The next question to answer is at level {level + 1}.")
    rows = [{"level": lv, "requires": ", ".join(k), "met": all(x in have for x in k)} for lv, k in LEVELS.items()]
    return r, "AI Adoption Maturity Self-Assessment", [("Scored levels", md_table(rows, ["level", "requires", "met"])),
                                                       ("First gap", md_table(gaps, ["level", "missing"]))], None


# ---------- Chapter 1 ----------
def _view():
    return ds("bq_ops_on_time_delivery_v.csv")


def grounded_agent(cfg, lab):
    """A deterministic stand-in for a grounded Gemini agent: answers only from approved sources, cites, or refuses."""
    r = new("1.1", "Grounded Enterprise Assistant Baseline")
    a, cat = cfg["agent"], cfg["source_catalogue"]
    for s in a["sources"]:
        meta = cat.get(s)
        if not meta or not meta.get("approved"):
            r.find("unapproved-source", f"{s} is not an approved grounding source in the catalogue.")
        elif meta.get("personal_information"):
            r.find("personal-data-source", f"{s} contains personal information (driver names, mobiles). Ground on the curated view.")
    if a.get("google_search_grounding"):
        r.find("open-web-grounding", "Grounding with Google Search is on. An internal operations agent must answer from enterprise data only.")
    view = {(x["depot"], x["month"]): x for x in _view()}
    rows = []
    for t in cfg["tests"]:
        hit = view.get((t.get("depot"), t.get("month"))) if "ops_on_time_delivery_v" in a["sources"] else None
        if hit:
            pct = round(100 * int(hit["on_time"]) / int(hit["deliveries"]), 1)
            out = {"behaviour": "answer", "answer": f"{pct}% on time", "citation": f"ops_curated.ops_on_time_delivery_v[{t['depot']},{t['month']}]"}
        elif a.get("google_search_grounding"):
            out = {"behaviour": "answer", "answer": "An industry average of about 90%", "citation": "web"}
        elif a.get("refuse_when_silent", False):
            out = {"behaviour": "refuse", "answer": "The approved source does not hold this. Escalating to the operations analyst.", "citation": ""}
        else:
            out = {"behaviour": "answer", "answer": "Probably around 90%", "citation": ""}
        if out["behaviour"] != t["expect"]:
            r.find("wrong-behaviour", f"'{t['q']}' expected {t['expect']} but agent did {out['behaviour']}.")
        if out["behaviour"] == "answer" and (not out["citation"] or out["citation"] == "web"):
            r.find("ungrounded-answer", f"'{t['q']}' answered without an enterprise citation.")
        rows.append({"question": t["q"], **out})
    return r, "Grounded Enterprise Assistant Baseline", [("Test transcript", md_table(rows, ["question", "behaviour", "answer", "citation"]))], None


def claim_cycle_hours():
    ev = {}
    for e in ds("claims_process_events.csv"):
        ev.setdefault(e["claim_id"], {})[e["step"]] = parse_ts(e["ts"])
    return statistics.median((v["paid"] - v["received"]).total_seconds() / 3600 for v in ev.values())


def process_baseline(cfg, lab):
    r = new("1.2", "Process Baseline and the 90-Day Plan")
    p = cfg["plan"]
    measured = round(claim_cycle_hours(), 1)
    r.data["measured_median_hours"] = measured
    if p.get("baseline_hours") in (None, ""):
        r.find("no-baseline", f"No baseline recorded. Measured median cycle time from the event log is {measured} hours.")
    elif abs(float(p["baseline_hours"]) - measured) / measured > 0.10:
        r.find("baseline-mismatch", f"Recorded baseline {p['baseline_hours']} differs from measured {measured} by more than 10%.")
    if not p.get("business_owner"):
        r.find("no-owner", "The process has no named business owner.")
    if not p.get("day_90_gate"):
        r.find("no-day-90-gate", "There is no Day 90 Gate date. A pilot without a decision date becomes a perpetual pilot.")
    if p.get("target_hours") and p.get("baseline_hours") and float(p["target_hours"]) >= float(p["baseline_hours"]):
        r.find("target-not-improvement", "The target is not better than the baseline.")
    return r, "Process Baseline and the 90-Day Plan", [("Plan", dump(p)), ("Measured", f"Median freight claim cycle time: **{measured} hours** (40 synthetic claims).")], None


# ---------- Chapter 2 ----------
def portfolio(cfg, lab):
    r = new("2.1", "Enterprise AI Portfolio Map")
    plats = cfg["platforms"]
    rows = []
    for w in cfg["workloads"]:
        p = plats.get(w["platform"])
        home = [n for n, x in plats.items() if w["data_location"] in x.get("home_data", [])]
        if not p:
            r.find("unknown-platform", f"{w['id']}: {w['platform']} is not on the map.")
            continue
        if not p.get("sanctioned"):
            r.find("unsanctioned-platform", f"{w['id']}: {w['platform']} is not sanctioned for enterprise data.")
        if not p.get("identity_boundary"):
            r.find("no-identity-boundary", f"{w['platform']} has no identity boundary recorded.")
        if home and w["platform"] not in home and not w.get("connector_justification"):
            r.find("placement-unjustified", f"{w['id']}: data lives in {w['data_location']} (home platform {', '.join(home)}) but is placed on {w['platform']} with no connector justification.")
        rows.append({"workload": w["id"], "data": w["data_location"], "platform": w["platform"], "home": ", ".join(home), "justification": w.get("connector_justification", "")})
    mmd = "flowchart LR\n" + "\n".join(f"  {x['workload'].replace('-', '_')}[{x['workload']}] --> {x['platform'].replace(' ', '_')}" for x in rows)
    return r, "Enterprise AI Portfolio Map", [("Placements", md_table(rows, ["workload", "data", "platform", "home", "justification"]))], {"portfolio-map.mmd": mmd}


def shadow_ai(cfg, lab):
    r = new("2.2", "Shadow AI Discovery")
    grants = ds("oauth_grants.csv") + (cfg.get("new_grants") or [])
    dec = cfg.get("decisions") or {}
    rows = []
    for g in grants:
        d = dec.get(g["app"], {})
        if g["sanctioned"] == "no" and g["data_access"] in ("drive", "gmail") and not d.get("decision"):
            r.find("unreviewed-ai-grant", f"{g['app']} has {g['scopes']} access for {g['users']} users and no decision.")
        if d.get("decision") == "review" and not d.get("owner"):
            r.find("no-owner", f"{g['app']} is under review with no named owner.")
        rows.append({**g, "decision": d.get("decision", ""), "owner": d.get("owner", "")})
    return r, "Shadow AI Discovery", [("OAuth grants and decisions", md_table(rows, ["app", "scopes", "users", "sanctioned", "decision", "owner"]))], None


# ---------- Chapter 3 ----------
VANITY = re.compile(r"(prompt|active user|licen[cs]e|usage|adoption rate|sessions)", re.I)


def value_hypothesis(cfg, lab):
    r = new("3.1", "Value Hypothesis and Baseline")
    h = cfg["hypothesis"]
    if VANITY.search(h.get("metric", "")) or h.get("metric_type") == "activity":
        r.find("vanity-metric", f"'{h.get('metric')}' measures activity, not a business number the CFO recognises.")
    if h.get("baseline") in (None, ""):
        r.find("no-baseline", "No measured baseline.")
    if h.get("baseline") not in (None, "") and h.get("target") not in (None, "") and h.get("direction", "down") == "down" and float(h["target"]) >= float(h["baseline"]):
        r.find("target-not-improvement", "Target does not improve on the baseline.")
    if not h.get("measured_by"):
        r.find("no-measurement-source", "No system of record named for measurement.")
    if not h.get("owner"):
        r.find("no-owner", "No accountable business owner.")
    return r, "Value Hypothesis and Baseline", [("Hypothesis", dump(h))], None


# ---------- Chapter 4 ----------
RUNGS = ["Buy", "Configure", "Integrate", "Build", "Host"]


def minimum_rung(w):
    if w.get("sovereign_hosting_required"):
        return "Host"
    if w.get("no_platform_fit"):
        return "Build"
    if w.get("acts_on_enterprise_systems"):
        return "Integrate"
    if w.get("workflow_specific"):
        return "Configure"
    return "Buy"


def decision_ladder(cfg, lab):
    r = new("4.1", "The Decision Ladder")
    rows = []
    for w in cfg["workloads"]:
        m = minimum_rung(w)
        c = w["chosen_rung"]
        if RUNGS.index(c) > RUNGS.index(m) and not w.get("justification"):
            r.find("over-engineered", f"{w['id']}: chose {c}, minimum is {m}, and no justification is recorded.")
        if RUNGS.index(c) < RUNGS.index(m):
            r.find("under-scoped", f"{w['id']}: chose {c} but the workload needs at least {m}.")
        rows.append({"workload": w["id"], "minimum": m, "chosen": c, "justification": w.get("justification", "")})
    return r, "The Decision Ladder", [("Rungs", md_table(rows, ["workload", "minimum", "chosen", "justification"]))], None


# ---------- Chapter 5 ----------
def architecture(cfg, lab):
    r = new("5.1", "Reference Architecture as Code")
    a = cfg["architecture"]
    for layer in ("productivity", "agent_experience", "build_and_run", "data_and_grounding", "security_and_governance"):
        if not a["layers"].get(layer):
            r.find("missing-layer", f"Layer '{layer}' has no components. Draw it, even if it is locked.")
    for ag in a["agents"]:
        ident = ag.get("identity", "")
        if not ident:
            r.find("no-agent-identity", f"{ag['name']} has no named identity.")
        elif "-compute@developer" in ident or "@appspot" in ident:
            r.find("default-service-account", f"{ag['name']} runs as a default service account ({ident}). Give it a dedicated, scoped identity.")
        if not ag.get("owner"):
            r.find("no-owner", f"{ag['name']} has no accountable owner.")
        if not ag.get("logging"):
            r.find("no-logging", f"{ag['name']} has no logging destination.")
        if ag.get("google_search_grounding") and ag.get("classification") == "internal":
            r.find("open-web-grounding", f"{ag['name']} is internal but grounds on Google Search.")
    lines = ["flowchart TB"]
    for layer, comps in a["layers"].items():
        lines.append(f"  subgraph {layer}")
        lines += [f"    {layer}_{i}[\"{c}\"]" for i, c in enumerate(comps)]
        lines.append("  end")
    for ag in a["agents"]:
        nid = ag["name"].replace(" ", "_")
        lines.append(f"  {nid}((\"{ag['name']}\")) -->|as {ag.get('identity', 'none')}| data_and_grounding")
    locked = md_table([{"component": c, "reason": x} for c, x in (a.get("locked") or {}).items()], ["component", "reason"])
    return r, "Reference Architecture as Code", [("Agents", md_table(a["agents"], ["name", "identity", "owner", "logging", "classification"])),
                                                 ("Left locked", locked), ("Diagram", "See reference-architecture.mmd (Mermaid source).")], {"reference-architecture.mmd": "\n".join(lines)}


def grounding_boundary(cfg, lab):
    r = new("5.2", "Grounding Boundary and Source Freshness")
    a = cfg["agent"]
    docs = [d for d in ds("policies.json") if a.get("include_superseded") or d["status"] == "current"]
    rows = []
    for t in cfg["tests"]:
        terms = set(t["q"].lower().split())
        scored = sorted(docs, key=lambda d: (-len(terms & set(d["text"].lower().replace(".", "").replace(":", "").split())), d["effective"]))
        best = scored[0] if scored and len(terms & set(scored[0]["text"].lower().split())) >= 2 else None
        if best:
            out = {"behaviour": "answer", "cited": f"{best['doc']} v{best['version']} ({best['status']})"}
            if best["status"] != "current":
                r.find("stale-source-cited", f"'{t['q']}' cited a superseded version: {out['cited']}.")
        elif a.get("refuse_when_silent"):
            out = {"behaviour": "refuse", "cited": ""}
        else:
            out = {"behaviour": "answer", "cited": "(model knowledge)"}
            r.find("no-refusal", f"'{t['q']}' is not covered by any source but the agent answered anyway.")
        if out["behaviour"] != t["expect"]:
            r.find("wrong-behaviour", f"'{t['q']}' expected {t['expect']}.")
        rows.append({"question": t["q"], **out})
    return r, "Grounding Boundary and Source Freshness", [("Transcript", md_table(rows, ["question", "behaviour", "cited"]))], None


# ---------- Chapter 6 ----------
def _files(cfg):
    files = {f["file_id"]: dict(f) for f in ds("drive_files.csv")}
    for f in cfg.get("new_files") or []:
        files[f["file_id"]] = dict(f)
    for fid, sharing in (cfg.get("remediation") or {}).items():
        if fid in files:
            files[fid]["sharing"] = sharing
    return files


def drive_exposure(cfg, lab):
    r = new("6.1", "Drive and Shared Drive Exposure Report")
    crown = set(cfg["crown_jewel_labels"])
    rows = []
    for f in _files(cfg).values():
        broad = f["sharing"] in ("domain", "anyone_with_link")
        if broad and f["label"] in crown:
            r.find("crown-jewel-exposed", f"{f['title']} ({f['label']}) is shared {f['sharing']}. Gemini will find it for anyone who can open it.", file=f["file_id"])
        elif f["sharing"] == "anyone_with_link":
            r.find("link-sharing", f"{f['title']} has an anyone-with-link share.", blocking=False)
        rows.append({**f, "broad": broad})
    dlp = cfg.get("dlp_rules") or []
    if not any(d.get("label") == "Confidential-HR" for d in dlp):
        r.find("no-dlp-rule", "No Workspace DLP rule protects Confidential-HR content from external sharing.")
    return r, "Drive and Shared Drive Exposure Report", [("Files", md_table(rows, ["file_id", "title", "label", "sharing", "broad"])),
                                                         ("DLP rules", md_table(dlp, ["name", "label", "action"]))], None


def agents_mirror(cfg, lab):
    r = new("6.2", "The Agent's Mirror")
    us, gs = users(), groups()
    for g, ms in (cfg.get("group_changes") or {}).items():
        gs.setdefault(g, set())
        for m in ms.get("add", []):
            gs[g].add(m)
        for m in ms.get("remove", []):
            gs[g].discard(m)
    who = cfg["query"]["user"]
    owning = {"Confidential-HR": {"People"}, "Board": {"Executive", "Legal"}}

    def can(f):
        s = f["sharing"]
        return s == "domain" or (s.startswith("group:") and who in gs.get(s[6:], set())) or f["owner"] == who

    terms = [t.lower() for t in cfg["query"]["terms"]]
    hits = [f for f in _files(cfg).values() if can(f) and any(t in f["title"].lower() for t in terms)]
    dept = us[who]["department"]
    for f in hits:
        if f["label"] in owning and dept not in owning[f["label"]]:
            r.find("sensitive-retrieval", f"{us[who]['name']} ({us[who]['role']}, {dept}) can have Gemini surface '{f['title']}' ({f['label']}) via {f['sharing']}.")
    r.data["results"] = [f["title"] for f in hits]
    return r, "The Agent's Mirror", [("Query", f"User **{who}** asks about: {', '.join(terms)}"),
                                     ("What the agent can surface", md_table(hits, ["title", "label", "sharing"]))], None


def identity_audit(cfg, lab):
    r = new("6.3", "Agent Identity and IAM Audit")
    iam = ds("iam_policy.json")["bindings"]
    rm = {(b["role"], b["member"], b["resource"]) for b in (cfg.get("remove_bindings") or [])}
    binds = [dict(role=b["role"], member=m, resource=b["resource"]) for b in iam for m in b["members"]
             if (b["role"], m, b["resource"]) not in rm] + list(cfg.get("add_bindings") or [])
    sas = {s["email"]: s for s in ds("service_accounts.json")}
    for e, ch in (cfg.get("sa_changes") or {}).items():
        sas[e] = {**sas.get(e, {"email": e, "keys": []}), **ch}
    us = users()
    for b in binds:
        sa = b["member"].split(":", 1)[1]
        if b["role"] in ("roles/owner", "roles/editor"):
            r.find("basic-role-on-agent", f"{sa} holds {b['role']} on {b['resource']}. Basic roles are never least privilege for an agent.")
        if b["resource"] in cfg.get("restricted_resources", []):
            r.find("raw-data-access", f"{sa} can read {b['resource']}, which holds personal information.")
    for e, s in sas.items():
        for k in s.get("keys", []):
            age = (TODAY - parse_date(k["created"])).days
            if k["type"] == "user_managed" and age > cfg.get("max_key_age_days", 90):
                r.find("stale-user-managed-key", f"{e} key {k['id']} is {age} days old. Prefer Workload Identity Federation or attached identities.")
        if s.get("agent") and s.get("owner") and us.get(s["owner"], {}).get("status") == "leaver":
            r.find("leaver-owner", f"{e} ({s['agent']}) is owned by a leaver ({s['owner']}).")
    return r, "Agent Identity and IAM Audit", [("Effective bindings", md_table(binds, ["member", "role", "resource"]))], None


# ---------- Chapter 7 ----------
def authority_gateway(cfg, lab):
    r = new("7.1", "Human-Agent Authority Matrix Gateway")
    m = cfg["matrix"]
    rows = []
    for q in cfg["requests"]:
        rule = m["actions"].get(q["action"])
        if q.get("channel") == "direct" and not m.get("gateway_only"):
            outcome = "executed (bypassed gateway)"
            r.find("gateway-bypass", f"{q['id']}: {q['action']} reached the system directly. The agent's identity must only reach tools through the gateway.")
        elif q.get("channel") == "direct":
            outcome = "rejected: network policy allows gateway only"
        elif not rule:
            outcome = "denied: action not in matrix"
        elif rule["agent"] == "never":
            outcome = "denied: human only"
        elif rule["agent"] == "approval" and (q.get("amount", 0) > rule.get("auto_limit", 0)) and not q.get("approval"):
            outcome = "held for approval"
        else:
            outcome = "executed"
            if q.get("consequential") and not q.get("approval") and q.get("amount", 0) > m.get("consequential_threshold", 0):
                r.find("unapproved-consequential-action", f"{q['id']}: {q['action']} for {q.get('amount')} executed with no human approval.")
        rows.append({"request": q["id"], "action": q["action"], "amount": q.get("amount", ""), "channel": q.get("channel", "gateway"), "outcome": outcome})
    for act in m.get("human_only", []):
        if m["actions"].get(act, {}).get("agent") != "never":
            r.find("matrix-invariant", f"{act} must be 'never' for agents.")
    return r, "Human-Agent Authority Matrix Gateway", [("Decisions", md_table(rows, ["request", "action", "amount", "channel", "outcome"]))], None


def function_calling(cfg, lab):
    r = new("7.2", "Gemini Function Calling Behind an Approval Gate")
    tools = {t["name"]: t for t in cfg["tools"]}
    for t in tools.values():
        if t.get("consequential") and not t.get("requires_approval"):
            r.find("consequential-tool-exposed", f"{t['name']} is consequential but declared to the model without an approval requirement.")
    rows = []
    for c in cfg["trace"]:
        t = tools.get(c["call"])
        verdict = "ok"
        if not t or c["call"] not in cfg["allowlist"]:
            verdict = "blocked: not allowlisted"
            if c.get("executed"):
                r.find("tool-not-allowlisted", f"{c['call']} executed but is not allowlisted.")
        elif t.get("requires_approval") and not c.get("approval_token"):
            verdict = "held: approval required"
            if c.get("executed"):
                r.find("call-without-approval", f"{c['call']} executed without an approval token.")
        elif t.get("max_amount") and c.get("args", {}).get("amount", 0) > t["max_amount"]:
            verdict = "blocked: argument outside schema"
            if c.get("executed"):
                r.find("argument-validation", f"{c['call']} amount {c['args']['amount']} exceeds {t['max_amount']}.")
        rows.append({"call": c["call"], "args": c.get("args", {}), "approval": c.get("approval_token", ""), "verdict": verdict})
    return r, "Gemini Function Calling Behind an Approval Gate", [("Function call trace", md_table(rows, ["call", "args", "approval", "verdict"]))], None


# ---------- Chapter 8 ----------
def inventory(cfg, lab):
    r = new("8.1", "Agent Inventory and Register")
    found = ds("agents.json") + (cfg.get("discovered_extra") or [])
    reg = {x["agent_id"]: x for x in cfg["register"]}
    us = users()
    rows = []
    for a in found:
        e = reg.get(a["agent_id"])
        if not e:
            r.find("unregistered-agent", f"{a['name']} ({a['surface']}) exists but is not in the Agent Register.")
            continue
        if us.get(e.get("owner"), {}).get("status") != "active":
            r.find("orphaned-agent", f"{a['name']} owner {e.get('owner')} is not an active employee.")
        if not e.get("risk_tier"):
            r.find("no-risk-tier", f"{a['name']} has no risk tier.")
        rows.append({**a, "register_owner": e.get("owner"), "risk_tier": e.get("risk_tier", "")})
    return r, "Agent Inventory and Register", [("Register reconciliation", md_table(rows, ["agent_id", "name", "surface", "register_owner", "risk_tier"]))], None


ASI = {"ASI01": "Agent goal hijack", "ASI02": "Tool misuse and exploitation", "ASI03": "Identity and privilege abuse",
       "ASI04": "Agentic supply chain vulnerabilities", "ASI05": "Unexpected code execution", "ASI06": "Memory and context poisoning",
       "ASI07": "Insecure inter-agent communication", "ASI08": "Cascading failures", "ASI09": "Human-agent trust exploitation",
       "ASI10": "Rogue agents"}


def threat_model(cfg, lab):
    r = new("8.2", "OWASP Agentic Threat Model")
    cat = set(cfg["control_catalogue"])
    rows = []
    for k, name in ASI.items():
        t = (cfg.get("threats") or {}).get(k) or {}
        ctl = t.get("controls") or []
        if not ctl:
            r.find("unmitigated-threat", f"{k} {name} has no control.")
        for c in ctl:
            if c not in cat:
                r.find("unknown-control", f"{k} cites '{c}', which is not in the control catalogue.")
        if ctl and not t.get("owner"):
            r.find("no-owner", f"{k} has controls but no owner.")
        rows.append({"id": k, "risk": name, "controls": ", ".join(ctl), "owner": t.get("owner", "")})
    return r, "OWASP Agentic Threat Model", [("Threat to control map", md_table(rows, ["id", "risk", "controls", "owner"]))], None


def detection(cfg, lab):
    r = new("8.3", "Logging, Detection and the Kill Switch")
    logs = ds("audit_logs.jsonl")
    rules = cfg["rules"]
    alerts = []
    for e in logs:
        for ru in rules:
            k = ru["type"]
            hit = ((k == "sensitive_dataset" and e.get("resource") in ru["resources"]) or
                   (k == "consequential_tool_without_approval" and e.get("method") == "tool.call" and not e.get("approval")) or
                   (k == "key_creation" and e.get("method") == "iam.serviceAccountKeys.create") or
                   (k == "volume" and e.get("rows", 0) > ru.get("threshold", 10 ** 9)))
            if hit:
                alerts.append({"rule": ru["id"], "ts": e["ts"], "principal": e["principal"], "resource": e["resource"]})
    suspicious = {e["ts"] for e in logs if e.get("resource") == "dataset:telematics_raw" or e.get("method") in ("tool.call", "iam.serviceAccountKeys.create")}
    caught = {a["ts"] for a in alerts}
    for ts in sorted(suspicious - caught):
        r.find("undetected-event", f"Suspicious event at {ts} raised no alert.")
    lg = cfg["logging"]
    if not lg.get("sink_enabled") or lg.get("retention_days", 0) < 365:
        r.find("logging-gap", f"Log sink enabled={lg.get('sink_enabled')}, retention {lg.get('retention_days')} days. Agent activity must be retained for at least 365 days.")
    ks = cfg["kill_switch"]
    if not ks.get("last_tested") or (TODAY - parse_date(ks["last_tested"])).days > 90:
        r.find("kill-switch-untested", "The kill switch has not been tested in the last 90 days.")
    return r, "Logging, Detection and the Kill Switch", [("Alerts", md_table(alerts, ["rule", "ts", "principal", "resource"])),
                                                         ("Kill switch", dump(ks))], None


REGISTRY = {"0.1": quick_start, "0.2": maturity, "1.1": grounded_agent, "1.2": process_baseline, "2.1": portfolio,
            "2.2": shadow_ai, "3.1": value_hypothesis, "4.1": decision_ladder, "5.1": architecture, "5.2": grounding_boundary,
            "6.1": drive_exposure, "6.2": agents_mirror, "6.3": identity_audit, "7.1": authority_gateway, "7.2": function_calling,
            "8.1": inventory, "8.2": threat_model, "8.3": detection}
