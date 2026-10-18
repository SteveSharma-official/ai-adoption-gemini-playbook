"""Lab engines for Parts III to V (Chapters 9 to 18) and the capstone."""
from __future__ import annotations
import hashlib, json, datetime as dt
from .core import new, ds, users, md_table, dump
from .common import parse_date

TODAY = dt.date(2026, 10, 18)


# ---------- Chapter 9 ----------
def discovery(cfg, lab):
    r = new("9.1", "Use-Case Discovery Canvas and Process Archaeology")
    rows = []
    for c in cfg["candidates"]:
        score = round(c["volume_per_month"] * c["hours_per_case"] * (1.0 if c["data_ready"] else 0.4) * (1.0 if c["rules_documented"] else 0.7))
        rows.append({**c, "score": score})
    rows.sort(key=lambda x: -x["score"])
    sel = [c for c in rows if c.get("selected")]
    if not sel:
        r.find("no-selection", "No process selected.")
    if len(sel) > 1:
        r.find("single-process-rule", f"{len(sel)} processes selected ({', '.join(c['id'] for c in sel)}). Prove one before you pilot three.")
    for c in sel:
        if not c.get("owner") or not c.get("baseline_measured"):
            r.find("selection-not-ready", f"{c['id']} lacks an owner or a measured baseline.")
        if c["id"] != rows[0]["id"] and not c.get("justification"):
            r.find("weaker-candidate", f"{c['id']} scores below {rows[0]['id']} and no justification is recorded.")
    return r, "Use-Case Discovery Canvas and Process Archaeology", [("Ranked candidates", md_table(rows, ["id", "name", "score", "owner", "baseline_measured", "selected"]))], None


# ---------- Chapter 10 ----------
def escalation(cfg, lab):
    r = new("10.1", "Escalation and Failure Paths")
    a = cfg["agent"]
    if not a.get("escalation_target"):
        r.find("no-escalation-target", "No named human queue for escalations.")
    rows = []
    for t in cfg["tests"]:
        if t.get("state") in a.get("escalate_states", []) or t["confidence"] < a["confidence_threshold"] or t.get("topic") in a.get("always_escalate_topics", []):
            got = "escalate"
        else:
            got = "answer"
        if t["expect"] == "escalate" and got == "answer":
            r.find("unsafe-answer", f"'{t['q']}' (state {t.get('state')}, confidence {t['confidence']}) was answered but should reach a person.")
        if t["expect"] == "answer" and got == "escalate":
            r.find("over-escalation", f"'{t['q']}' escalated unnecessarily.", blocking=False)
        rows.append({"question": t["q"], "state": t.get("state", ""), "confidence": t["confidence"], "expected": t["expect"], "got": got})
    esc = sum(1 for x in rows if x["got"] == "escalate")
    r.data["escalation_rate"] = round(esc / len(rows), 2)
    return r, "Escalation and Failure Paths", [("Test results", md_table(rows, ["question", "state", "confidence", "expected", "got"]))], None


# ---------- Chapter 11 ----------
def pilot_gate(cfg, lab):
    r = new("11.1", "Pilot Charter and the Day 90 Gate")
    ch, m = cfg["charter"], cfg["measured"]
    safety_ok = all(m.get(k, 0) >= v for k, v in ch["safety_floors"].items())
    value = (ch["baseline"] - m["value_metric"]) / (ch["baseline"] - ch["target"])
    readiness = m.get("readiness_signed", False)
    computed = "Stop" if not safety_ok else ("Go" if value >= 1 and readiness else ("Extend" if value >= 0.5 else "Stop"))
    r.data.update(value_realised=round(value, 2), safety_ok=safety_ok, computed=computed, recorded=cfg.get("decision"))
    if cfg.get("decision") != computed:
        r.find("gate-decision-unsupported", f"Recorded decision '{cfg.get('decision')}' but the evidence supports '{computed}' (value realised {value:.0%}, safety floors met: {safety_ok}).")
    if not ch.get("executive_sponsor"):
        r.find("no-sponsor", "No executive sponsor committed to attend the gate.")
    return r, "Pilot Charter and the Day 90 Gate", [("Charter", dump(ch)), ("Measured", dump(m))], None


# ---------- Chapter 12 ----------
def evaluation(cfg, lab):
    r = new("12.1", "Evaluation Harness")
    resp = {x["id"]: x for x in cfg["responses"]}
    cases = cfg["testset"]
    def rate(key, subset):
        s = [resp[c["id"]][key] for c in subset if c["id"] in resp]
        return round(sum(s) / len(s), 3) if s else 0
    core = [c for c in cases if c["category"] == "core"]
    scores = {"task_success": rate("task_success", core), "groundedness": rate("grounded", core),
              "safety": rate("safe", [c for c in cases if c["category"] == "safety"]),
              "escalation": rate("escalated", [c for c in cases if c["category"] == "edge"])}
    for k, th in cfg["thresholds"].items():
        if scores[k] < th:
            r.find("below-threshold", f"{k} {scores[k]:.1%} is below the threshold {th:.0%}.")
        base = (cfg.get("baseline_scores") or {}).get(k)
        if base is not None and scores[k] < base - 0.02:
            r.find("regression", f"{k} fell from {base:.1%} to {scores[k]:.1%} against the last release.")
    r.data["scores"] = scores
    rows = [{"metric": k, "score": v, "threshold": cfg["thresholds"][k], "baseline": (cfg.get("baseline_scores") or {}).get(k, "")} for k, v in scores.items()]
    return r, "Evaluation Harness", [("Scorecard", md_table(rows, ["metric", "score", "threshold", "baseline"])),
                                     ("Note", "Thresholds are author recommendations set by risk tier, not industry standards. A failed citation match is not automatically a hallucination: review each failure.")], {"scores.json": json.dumps(scores, indent=2)}


def red_team(cfg, lab):
    r = new("12.2", "Red Team: Direct and Indirect Prompt Injection")
    d = cfg["defences"]
    block = {"direct": d.get("input_screening"), "indirect_drive": d.get("retrieved_content_as_data") or d.get("screen_retrieved_content"),
             "tool_argument": d.get("tool_gating"), "exfiltration": d.get("output_screening")}
    rows = []
    for a in cfg["attacks"]:
        ok = not block.get(a["vector"])
        if ok:
            r.find("injection-succeeded", f"{a['id']} ({a['vector']}): {a['goal']} succeeded.")
        rows.append({"attack": a["id"], "vector": a["vector"], "goal": a["goal"], "result": "SUCCEEDED" if ok else "blocked"})
    return r, "Red Team: Direct and Indirect Prompt Injection", [("Defences", dump(d)), ("Attack results", md_table(rows, ["attack", "vector", "goal", "result"]))], None


def readiness(cfg, lab):
    r = new("12.3", "Production Readiness Gate")
    rows = []
    for it in cfg["checklist"]:
        p = lab / it["evidence"]
        ok = p.exists() and p.stat().st_size > 0
        if not ok:
            r.find("missing-evidence", f"'{it['item']}' claims evidence at {it['evidence']} but the file is missing.")
        if not it.get("signed_by"):
            r.find("not-signed", f"'{it['item']}' has no sign-off.")
        rows.append({"item": it["item"], "evidence": it["evidence"], "present": ok, "signed_by": it.get("signed_by", "")})
    return r, "Production Readiness Gate", [("Gate", md_table(rows, ["item", "evidence", "present", "signed_by"]))], None


# ---------- Chapter 13 ----------
def chain(records):
    prev, out = "0" * 64, []
    for rec in records:
        body = json.dumps(rec, sort_keys=True)
        h = hashlib.sha256((prev + body).encode()).hexdigest()
        out.append({**rec, "prev": prev, "hash": h})
        prev = h
    return out


def verify(chained):
    prev = "0" * 64
    for rec in chained:
        body = {k: v for k, v in rec.items() if k not in ("prev", "hash")}
        if rec["prev"] != prev or hashlib.sha256((prev + json.dumps(body, sort_keys=True)).encode()).hexdigest() != rec["hash"]:
            return False
        prev = rec["hash"]
    return True


def fs_router(cfg, lab):
    r = new("13.1", "Financial Services Hardship Router and Agentic Audit Trail")
    kw = [k.lower() for k in cfg["router"]["hardship_keywords"]]
    recs = []
    for c in cfg["cases"]:
        hardship = any(k in c["message"].lower() for k in kw)
        action = cfg["agent"]["action_for"].get(c["request"], "prepare_summary")
        route = cfg["router"]["route_to"] if hardship else "standard queue"
        if hardship and cfg["router"].get("enabled") is False:
            route = "standard queue"
            r.find("hardship-not-routed", f"{c['id']} shows hardship indicators but was not routed to the hardship team.")
        if action in ("approve_credit", "decline_credit"):
            r.find("credit-decision-by-agent", f"{c['id']}: the agent performed {action}. Credit decisions stay with an accountable person.")
        recs.append({"case": c["id"], "hardship": hardship, "agent_action": action, "routed_to": route, "model": cfg["agent"]["model_version"], "sources": c.get("sources", [])})
    trail = chain(recs)
    for t in cfg.get("tamper") or []:
        trail[t["index"]][t["field"]] = t["value"]
    if not verify(trail):
        r.find("audit-chain-broken", "The Agentic Audit Trail hash chain does not verify. A record was changed after it was written.")
    return r, "Financial Services Hardship Router and Agentic Audit Trail", [("Decisions", md_table(recs, ["case", "hardship", "agent_action", "routed_to"]))], {"agentic-audit-trail.jsonl": "\n".join(json.dumps(x) for x in trail)}


# ---------- Chapter 14 ----------
def clinical(cfg, lab):
    r = new("14.1", "Clinical Safety Router")
    a = cfg["agent"]
    rows = []
    for x in cfg["results"]:
        critical = x["value"] >= x["critical_at"]
        route = cfg["router"].get("critical_route") if critical else "routine review"
        if critical and (not route or cfg["router"].get("max_minutes", 999) > 30):
            r.find("critical-not-routed", f"{x['patient']} {x['test']} {x['value']} is critical and is not routed to a clinician within 30 minutes.")
        rows.append({"patient": x["patient"], "test": x["test"], "value": x["value"], "critical": critical, "route": route})
    for o in cfg["agent_outputs"]:
        if o["type"] not in a["allowed_outputs"]:
            r.find("clinical-decision-by-agent", f"Agent produced '{o['type']}' for {o['patient']}. Only {', '.join(a['allowed_outputs'])} are permitted; the clinician signs.")
    return r, "Clinical Safety Router", [("Results routing", md_table(rows, ["patient", "test", "value", "critical", "route"])),
                                         ("Agent outputs", md_table(cfg["agent_outputs"], ["patient", "type"]))], None


# ---------- Chapter 15 ----------
TR_FIELDS = ["purpose", "human_decision_maker", "data_used", "how_ai_is_used", "review_rights", "contact"]


def public_authority(cfg, lab):
    r = new("15.1", "Public Authority Line and Transparency Record")
    for a in cfg["applications"]:
        if a["adverse"] and a["decided_by"] != "human":
            r.find("automated-adverse-decision", f"{a['id']}: an adverse outcome ({a['outcome']}) was decided by {a['decided_by']}. A delegated officer must decide.")
        if a["decided_by"] == "human" and not a.get("reasons_recorded"):
            r.find("no-reasons", f"{a['id']}: no statement of reasons recorded.")
    tr = cfg.get("transparency_record") or {}
    miss = [f for f in TR_FIELDS if not tr.get(f)]
    if miss:
        r.find("transparency-record-incomplete", f"Transparency Record is missing: {', '.join(miss)}.")
    return r, "Public Authority Line and Transparency Record", [("Applications", md_table(cfg["applications"], ["id", "outcome", "adverse", "decided_by", "reasons_recorded"])),
                                                                ("Transparency Record", dump(tr))], {"transparency-record.json": json.dumps(tr, indent=2)}


def sovereign(cfg, lab):
    r = new("15.2", "Sovereign Hosting Boundary Check")
    d = cfg["deployment"]
    scope = set(cfg["irap_products_in_scope"])
    acc = d.get("confirmations") or {}
    for s in d["services"]:
        if s not in scope and s not in acc:
            r.find("outside-irap-scope", f"'{s}' is not on the published IRAP in-scope list under that name, and no confirmation or risk acceptance is recorded.")
    for k in ("data_region", "model_endpoint_region"):
        if d.get(k) not in cfg["allowed_regions"]:
            r.find("residency-breach", f"{k} is '{d.get(k)}'. Allowed: {', '.join(cfg['allowed_regions'])}.")
    if not (d.get("agency_authorisation") or {}).get("date"):
        r.find("no-agency-authorisation", "No agency authorisation decision recorded. An IRAP report informs that decision; it does not replace it.")
    return r, "Sovereign Hosting Boundary Check", [("Deployment", dump(d))], None


# ---------- Chapter 16 ----------
def ot_boundary(cfg, lab):
    r = new("16.1", "IT and OT Boundary")
    rows = []
    for t in cfg["tools"]:
        zone = t["zone"]
        if t["access"] == "write" and zone in ("L0", "L1", "L2", "L3"):
            r.find("ot-write-path", f"{t['name']} can write to {zone}. No AI agent writes to a control system.")
        if t["access"] == "read" and zone in ("L1", "L2"):
            r.find("ot-direct-read", f"{t['name']} reads {zone} directly. Read from the historian replica in the DMZ ({cfg['dmz_zone']}).")
        rows.append(t)
    return r, "IT and OT Boundary", [("Agent tools by Purdue zone", md_table(rows, ["name", "zone", "access", "purpose"]))], None


def retail(cfg, lab):
    r = new("16.2", "Retail Pricing and Refund Rules")
    rules = cfg["rules_engine"]
    rows = []
    for q in cfg["requests"]:
        if "vulnerable" in q.get("flags", []):
            out = "routed to specialist team" if rules.get("route_vulnerable") else "handled by agent"
            if not rules.get("route_vulnerable"):
                r.find("vulnerable-not-routed", f"{q['id']}: a vulnerable customer was handled by the agent.")
        elif q["type"] == "price_change":
            out = "executed by agent" if "price_change" in cfg["agent_can_execute"] else "proposed to pricing manager"
        elif q["type"] == "refund":
            out = "executed by agent" if q["amount"] <= rules["refund_auto_limit"] and "refund" in cfg["agent_can_execute"] else "proposed to team leader"
            if q["amount"] > rules["refund_auto_limit"] and "refund_any" in cfg["agent_can_execute"]:
                out = "executed by agent"
        else:
            out = "answered"
        if out == "executed by agent" and (q["type"] == "price_change" or q.get("amount", 0) > rules["refund_auto_limit"]):
            r.find("commercial-decision-by-agent", f"{q['id']}: the agent executed a {q['type']} the rules engine reserves for a person.")
        rows.append({"request": q["id"], "type": q["type"], "amount": q.get("amount", ""), "outcome": out})
    return r, "Retail Pricing and Refund Rules", [("Outcomes", md_table(rows, ["request", "type", "amount", "outcome"]))], None


# ---------- Chapter 17 ----------
def operating_model(cfg, lab):
    r = new("17.1", "Operating Model RACI, Runbook and Kill Switch Drill")
    us = users()
    rows = []
    for a in ds("agents.json"):
        if a["agent_id"] not in cfg["in_scope"]:
            continue
        rc = cfg["raci"].get(a["agent_id"], {})
        acc = rc.get("accountable")
        if not acc or us.get(acc, {}).get("status") != "active":
            r.find("no-accountable-owner", f"{a['name']}: accountable person '{acc}' is missing or has left.")
        rb = cfg["runbook"].get(a["agent_id"], {})
        if not rb.get("disable_steps"):
            r.find("runbook-missing-disable", f"{a['name']}: the runbook has no disable steps the service desk can follow.")
        drill = rb.get("last_drill")
        if not drill or (TODAY - parse_date(drill)).days > 90:
            r.find("drill-overdue", f"{a['name']}: kill switch drill last run {drill}.")
        rows.append({"agent": a["name"], "accountable": acc, "responsible": rc.get("responsible"), "last_drill": drill})
    return r, "Operating Model RACI, Runbook and Kill Switch Drill", [("RACI", md_table(rows, ["agent", "accountable", "responsible", "last_drill"]))], None


def change_pipeline(cfg, lab):
    r = new("17.2", "Agent Change Pipeline")
    for c in cfg["changes"]:
        mv = str(c.get("model_version", ""))
        if not mv or mv.endswith("latest") or mv == "auto":
            r.find("unpinned-model", f"{c['id']}: model version '{mv}' is not pinned. Pin it so evaluation results stay valid.")
        if c.get("deployed") and not c.get("eval_passed"):
            r.find("deployed-without-eval", f"{c['id']}: deployed without a passing evaluation run.")
        if c["type"] == "tool" and not c.get("approved_by"):
            r.find("unapproved-change", f"{c['id']}: a tool change needs CAB or risk approval.")
    return r, "Agent Change Pipeline", [("Changes", md_table(cfg["changes"], ["id", "type", "model_version", "eval_passed", "approved_by", "deployed"]))], None


def finops(cfg, lab):
    r = new("17.3", "FinOps Cost Model")
    g = cfg["guardrails"]
    if not g.get("budget_alerts") or not g.get("monthly_cap"):
        r.find("no-budget-guardrail", "No budget alert thresholds or monthly cap on the agent project.")
    rows = []
    for a in cfg["agents"]:
        cost = a["monthly_calls"] * a["cost_per_call"]
        value = a["outcomes_per_month"] * a["value_per_outcome"]
        if cost > value:
            r.find("cost-exceeds-value", f"{a['name']}: monthly cost {cost:,.0f} exceeds measured value {value:,.0f}.")
        rows.append({"agent": a["name"], "monthly_cost": round(cost), "monthly_value": round(value), "cost_per_outcome": round(cost / max(a["outcomes_per_month"], 1), 2)})
    lic = cfg.get("licences") or {}
    if lic and lic["active"] / lic["seats"] < 0.6:
        r.find("idle-licences", f"{lic['active']} of {lic['seats']} seats active.", blocking=False)
    return r, "FinOps Cost Model", [("Unit economics (illustrative prices, not Google list prices)", md_table(rows, ["agent", "monthly_cost", "monthly_value", "cost_per_outcome"]))], None


# ---------- Chapter 18 ----------
def portfolio_scale(cfg, lab):
    r = new("18.1", "Portfolio Prioritisation and Executive Dashboard")
    shared = set(cfg["shared_platform"])
    rows = []
    for b in cfg["backlog"]:
        dup = [x for x in b.get("bespoke", []) if x in shared]
        if dup:
            r.find("platform-bypass", f"{b['id']} builds its own {', '.join(dup)} instead of using the Shared Platform Model.")
        score = round(b["value"] * (6 - b["risk"]) / b["effort"], 1)
        rows.append({"id": b["id"], "name": b["name"], "score": score, "reuses": ", ".join(b.get("uses", [])), "bespoke": ", ".join(b.get("bespoke", []))})
    rows.sort(key=lambda x: -x["score"])
    for m in cfg["dashboard"]:
        if not m.get("source"):
            r.find("metric-without-source", f"Dashboard metric '{m['metric']}' has no system of record.")
    return r, "Portfolio Prioritisation and Executive Dashboard", [("Prioritised backlog", md_table(rows, ["id", "name", "score", "reuses", "bespoke"])),
                                                                   ("Executive Dashboard", md_table(cfg["dashboard"], ["metric", "source", "owner"]))], None


# ---------- Capstone ----------
def capstone(cfg, lab):
    r = new("Capstone", "Enterprise Gemini Adoption Capstone")
    c = cfg["case"]
    gates = [
        ("process-and-baseline", c["baseline_hours"] and c["process_owner"]),
        ("portfolio-placement", c["platform"] in c["home_platforms_for_data"] or c.get("connector_justification")),
        ("exposure-remediated", c["crown_jewels_broadly_shared"] == 0),
        ("scoped-identity", c["agent_identity"] and not c["agent_has_basic_role"]),
        ("authority-matrix", all(a["agent"] in ("never", "approval") for a in c["consequential_actions"])),
        ("evaluation", all(c["scores"][k] >= v for k, v in c["thresholds"].items())),
        ("red-team", c["red_team_successes"] == 0),
        ("logging-and-kill-switch", c["log_retention_days"] >= 365 and c["kill_switch_tested"]),
        ("value", c["measured_hours"] <= c["target_hours"]),
        ("operating-model", bool(c["accountable_owner"]) and bool(c["runbook"])),
    ]
    rows = []
    for name, ok in gates:
        if not ok:
            r.find("capstone-gate", f"Gate '{name}' is not met.")
        rows.append({"gate": name, "met": bool(ok)})
    verdict = "Go" if r.passed else "Not ready"
    r.data["verdict"] = verdict
    return r, "Enterprise Gemini Adoption Capstone", [("Production readiness gates", md_table(rows, ["gate", "met"])),
                                                      ("Day 90 verdict", f"**{verdict}**")], None


REGISTRY = {"9.1": discovery, "10.1": escalation, "11.1": pilot_gate, "12.1": evaluation, "12.2": red_team, "12.3": readiness,
            "13.1": fs_router, "14.1": clinical, "15.1": public_authority, "15.2": sovereign, "16.1": ot_boundary, "16.2": retail,
            "17.1": operating_model, "17.2": change_pipeline, "17.3": finops, "18.1": portfolio_scale, "Capstone": capstone}
