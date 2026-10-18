#!/usr/bin/env python3
"""Generate the synthetic Kestrel Freight Group dataset used by every lab.

Kestrel Freight Group is fictional (domain kestrel.example). It runs Google Workspace for most staff,
BigQuery for telematics and operations data, and Microsoft 365 in its acquired Customs Brokerage division.
Deterministic: the same seed always produces the same files.

  python shared/scripts/generate_datasets.py
"""
import csv, json, random, datetime as dt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datasets" / "kestrel"
R = random.Random(20261018)
TODAY = dt.date(2026, 10, 18)

FIRST = ["Ava", "Liam", "Mia", "Noah", "Isla", "Jack", "Zara", "Ethan", "Ruby", "Arjun", "Chloe", "Leo", "Priya", "Tom", "Grace",
         "Sam", "Nina", "Omar", "Ella", "Ben", "Hana", "Luca", "Maya", "Ravi", "Sofia", "Kai", "Lily", "Max", "Aria", "Dev"]
LAST = ["Nguyen", "Smith", "Patel", "Brown", "Wilson", "Chen", "Taylor", "Singh", "Martin", "Kelly", "Rossi", "Walker",
        "Khan", "Lee", "Murphy", "Hall", "Young", "King", "Wright", "Scott"]
DEPTS = [("Operations", "VIC"), ("Finance", "VIC"), ("People", "NSW"), ("Fleet Engineering", "QLD"), ("Customer Service", "NSW"),
         ("Customs Brokerage", "WA"), ("Executive", "VIC"), ("IT and Security", "VIC"), ("Sales", "QLD"), ("Legal", "VIC")]


def w(name, rows, cols):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    users = []
    for i in range(1, 61):
        d, st = DEPTS[(i - 1) % len(DEPTS)]
        users.append({"user_id": f"u{i:03d}", "name": f"{FIRST[(i * 7) % 30]} {LAST[(i * 3) % 20]}",
                      "email": f"u{i:03d}@kestrel.example", "department": d, "state": st,
                      "role": "Graduate" if i in (12, 33) else ("Manager" if i % 10 == 1 else "Staff"),
                      "status": "leaver" if i in (27, 48) else "active"})
    w("users.csv", users, list(users[0]))

    groups = {"all-staff": [u["user_id"] for u in users],
              "finance-team": [u["user_id"] for u in users if u["department"] == "Finance"],
              "people-team": [u["user_id"] for u in users if u["department"] == "People"],
              "executive": [u["user_id"] for u in users if u["department"] == "Executive"],
              "fleet-eng": [u["user_id"] for u in users if u["department"] == "Fleet Engineering"],
              "all-finance-readers": ["u002", "u022", "u042"]}
    w("group_members.csv", [{"group": g, "user_id": m} for g, ms in groups.items() for m in ms], ["group", "user_id"])

    files = [
        ("f001", "2019 Salary Review Workbook", "People Shared", "u003", "Confidential-HR", "domain"),
        ("f002", "Executive Remuneration 2026", "People Shared", "u003", "Confidential-HR", "group:people-team"),
        ("f003", "Board Pack October 2026", "Board", "u007", "Board", "group:executive"),
        ("f004", "Board Pack September 2026", "Board", "u007", "Board", "anyone_with_link"),
        ("f005", "FY27 Budget Model", "Finance Shared", "u002", "Finance", "group:finance-team"),
        ("f006", "Supplier Bank Details Register", "Finance Shared", "u002", "Finance", "domain"),
        ("f007", "Driver Medical Clearances", "People Shared", "u013", "Confidential-HR", "group:people-team"),
        ("f008", "Fleet Maintenance SOP v4", "Fleet Engineering", "u004", "Internal", "domain"),
        ("f009", "Customer Rate Card 2026", "Sales", "u009", "Internal", "domain"),
        ("f010", "Acquisition Target Shortlist", "Legal", "u010", "Board", "group:executive"),
        ("f011", "Leave Policy (current)", "People Shared", "u003", "Internal", "domain"),
        ("f012", "Office Relocation FAQ", "Operations", "u001", "Public", "domain"),
        ("f013", "Payroll Exceptions Q3", "Finance Shared", "u022", "Confidential-HR", "group:all-finance-readers"),
        ("f014", "Incident Postmortem Telematics Outage", "IT and Security", "u008", "Internal", "group:all-staff"),
    ]
    w("drive_files.csv", [dict(zip(["file_id", "title", "shared_drive", "owner", "label", "sharing"], f)) for f in files],
      ["file_id", "title", "shared_drive", "owner", "label", "sharing"])

    sas = [
        {"email": "freight-assistant@kestrel-ops.iam.gserviceaccount.com", "agent": "Freight Ops Assistant", "owner": "u001",
         "keys": [{"id": "k1", "type": "user_managed", "created": "2025-11-02"}]},
        {"email": "hr-answers@kestrel-ops.iam.gserviceaccount.com", "agent": "HR Answers Agent", "owner": "u027", "keys": []},
        {"email": "procure-agent@kestrel-ops.iam.gserviceaccount.com", "agent": "Procurement Agent", "owner": "u002",
         "keys": [{"id": "k2", "type": "user_managed", "created": "2026-09-30"}]},
        {"email": "123456789-compute@developer.gserviceaccount.com", "agent": None, "owner": None, "keys": []},
    ]
    (OUT / "service_accounts.json").write_text(json.dumps(sas, indent=2))
    iam = {"project": "kestrel-ops", "bindings": [
        {"role": "roles/bigquery.dataViewer", "members": ["serviceAccount:freight-assistant@kestrel-ops.iam.gserviceaccount.com"],
         "resource": "dataset:ops_curated"},
        {"role": "roles/bigquery.dataViewer", "members": ["serviceAccount:freight-assistant@kestrel-ops.iam.gserviceaccount.com"],
         "resource": "dataset:telematics_raw"},
        {"role": "roles/editor", "members": ["serviceAccount:hr-answers@kestrel-ops.iam.gserviceaccount.com"], "resource": "project"},
        {"role": "roles/aiplatform.user", "members": ["serviceAccount:procure-agent@kestrel-ops.iam.gserviceaccount.com"],
         "resource": "project"},
        {"role": "roles/editor", "members": ["serviceAccount:123456789-compute@developer.gserviceaccount.com"], "resource": "project"},
    ]}
    (OUT / "iam_policy.json").write_text(json.dumps(iam, indent=2))

    depots = ["Melbourne West", "Sydney Airport", "Brisbane Port", "Perth Kewdale", "Adelaide North"]
    rows = []
    for m in range(1, 10):
        for d in depots:
            planned = R.randint(800, 1400)
            rows.append({"month": f"2026-{m:02d}", "depot": d, "deliveries": planned,
                         "on_time": int(planned * R.uniform(0.86, 0.97))})
    w("bq_ops_on_time_delivery_v.csv", rows, ["month", "depot", "deliveries", "on_time"])
    raw = [{"ts": f"2026-09-{d:02d}T0{R.randint(5, 9)}:00:00", "truck": f"KT{R.randint(100, 199)}",
            "driver_name": f"{FIRST[R.randint(0, 29)]} {LAST[R.randint(0, 19)]}", "driver_mobile": f"04{R.randint(10000000, 99999999)}",
            "lat": round(-37.8 + R.uniform(-1, 1), 4), "lon": round(144.9 + R.uniform(-1, 1), 4)} for d in range(1, 21)]
    w("bq_telematics_raw.csv", raw, list(raw[0]))

    policies = [
        {"doc": "leave-policy", "version": 3, "status": "superseded", "effective": "2023-07-01",
         "text": "Parental leave: 12 weeks paid primary carer leave for all staff."},
        {"doc": "leave-policy", "version": 4, "status": "current", "effective": "2025-07-01",
         "text": "Parental leave: 18 weeks paid primary carer leave. State award variations apply in WA; refer WA staff to People team."},
        {"doc": "travel-policy", "version": 2, "status": "current", "effective": "2025-01-01",
         "text": "Interstate travel requires manager approval and economy fares under 1000 dollars."},
        {"doc": "fleet-sop", "version": 4, "status": "current", "effective": "2026-02-01",
         "text": "Brake inspection every 20000 km. Lock out and tag out before any hydraulic work."},
    ]
    (OUT / "policies.json").write_text(json.dumps(policies, indent=2))

    events = []
    for c in range(1, 41):
        start = dt.datetime(2026, 7, 1, 9) + dt.timedelta(days=c, hours=R.randint(0, 6))
        steps = [("received", 0), ("evidence_gathered", R.randint(20, 70)), ("assessed", R.randint(10, 40)),
                 ("approved", R.randint(5, 30)), ("paid", R.randint(30, 90))]
        t = start
        for s, gap in steps:
            t = t + dt.timedelta(hours=gap)
            events.append({"claim_id": f"CL{c:03d}", "step": s, "ts": t.isoformat()})
    w("claims_process_events.csv", events, ["claim_id", "step", "ts"])

    grants = [
        {"app": "Gemini (sanctioned)", "scopes": "workspace", "users": 58, "sanctioned": "yes", "data_access": "drive"},
        {"app": "MeetNotes AI", "scopes": "drive.readonly calendar", "users": 14, "sanctioned": "no", "data_access": "drive"},
        {"app": "PDF Chat Pro", "scopes": "drive.file", "users": 6, "sanctioned": "no", "data_access": "drive"},
        {"app": "Grammar Helper", "scopes": "gmail.compose", "users": 9, "sanctioned": "no", "data_access": "gmail"},
    ]
    w("oauth_grants.csv", grants, list(grants[0]))

    audit = []
    base = dt.datetime(2026, 10, 14, 8)
    for i in range(40):
        audit.append({"ts": (base + dt.timedelta(minutes=17 * i)).isoformat(), "principal": "freight-assistant@kestrel-ops.iam.gserviceaccount.com",
                      "method": "bigquery.jobs.query", "resource": "dataset:ops_curated", "rows": R.randint(5, 200)})
    audit.append({"ts": "2026-10-15T02:11:00", "principal": "freight-assistant@kestrel-ops.iam.gserviceaccount.com",
                  "method": "bigquery.jobs.query", "resource": "dataset:telematics_raw", "rows": 48210})
    audit.append({"ts": "2026-10-15T02:14:00", "principal": "procure-agent@kestrel-ops.iam.gserviceaccount.com",
                  "method": "tool.call", "resource": "erp:create_purchase_order", "amount": 48000, "approval": None})
    audit.append({"ts": "2026-10-15T09:30:00", "principal": "u027@kestrel.example", "method": "iam.serviceAccountKeys.create",
                  "resource": "hr-answers@kestrel-ops.iam.gserviceaccount.com"})
    (OUT / "audit_logs.jsonl").write_text("\n".join(json.dumps(a) for a in audit) + "\n")

    agents = [
        {"agent_id": "ag-01", "name": "Freight Ops Assistant", "owner": "u001", "surface": "Gemini Enterprise app", "status": "pilot"},
        {"agent_id": "ag-02", "name": "HR Answers Agent", "owner": "u027", "surface": "Gemini Enterprise app", "status": "pilot"},
        {"agent_id": "ag-03", "name": "Procurement Agent", "owner": "u002", "surface": "Agent Platform (ADK)", "status": "build"},
        {"agent_id": "ag-04", "name": "Quote Drafting Gem", "owner": "u009", "surface": "Gemini app (Gem)", "status": "in use"},
        {"agent_id": "ag-05", "name": "Customs Doc Checker", "owner": "u048", "surface": "Agent Platform (ADK)", "status": "in use"},
    ]
    (OUT / "agents.json").write_text(json.dumps(agents, indent=2))
    print(f"Wrote Kestrel Freight Group dataset to {OUT}")


if __name__ == "__main__":
    main()
