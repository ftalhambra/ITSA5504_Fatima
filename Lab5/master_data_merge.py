"""
master_data_merge.py
Simulates merging two source systems (CRM + ERP) into a single golden record.
Prints the golden record and per-field provenance, and writes golden_record.json
"""

import json
from datetime import datetime, timezone


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def pick_scalar(sources, field):
    candidates = [s for s in sources if s.get(field) not in (None, "", [])]
    if not candidates:
        return None, None
    src = max(candidates, key=lambda s: parse_ts(s.get("updated_at", "1970-01-01T00:00:00Z")))
    return src.get(field), src["system"]


def merge_addresses(sources):
    by_type = {}
    provenance = {}
    for s in sources:
        ts = parse_ts(s.get("updated_at", "1970-01-01T00:00:00Z"))
        for addr in s.get("addresses", []):
            t = addr.get("type", "unknown")
            if (t not in by_type) or (ts > by_type[t]["_ts"]):
                by_type[t] = {**addr, "_ts": ts, "_src": s["system"]}
    merged = []
    for t, rec in by_type.items():
        src = rec.pop("_src")
        rec.pop("_ts")
        merged.append(rec)
        provenance[t] = src
    return merged, provenance


def merge_external_ids(sources):
    merged = {}
    for s in sources:
        for k, v in s.get("external_ids", {}).items():
            merged[k] = v
    return merged or None


def main():
    crm = {
        "system": "CRM",
        "customer_id": "CUST-1001",
        "first_name": "Amina",
        "last_name": "Rahman",
        "email": "amina.r@example.com",
        "addresses": [
            {"type": "home", "line1": "123 Bloor St W", "city": "Toronto", "province": "ON", "postal_code": "M5S 1W7", "country": "CA"}
        ],
        "updated_at": "2026-02-11T09:00:00Z",
    }

    erp = {
        "system": "ERP",
        "customer_id": "1001",
        "first_name": "Amina",
        "last_name": "Rahman",
        "email": "amina.rahman@example.com",
        "phone": "+1-416-555-0197",
        "addresses": [
            {"type": "billing", "line1": "400 King St E", "city": "Toronto", "province": "ON", "postal_code": "M5A 1L7", "country": "CA"}
        ],
        "external_ids": {"crm": "CUST-1001", "erp": "1001"},
        "updated_at": "2026-02-12T08:30:00Z",
    }

    sources = [crm, erp]

    canonical_id = crm.get("customer_id") or erp.get("customer_id")

    golden = {
        "customer_id": canonical_id,
        "first_name": pick_scalar(sources, "first_name")[0],
        "last_name": pick_scalar(sources, "last_name")[0],
        "email": pick_scalar(sources, "email")[0],
        "phone": pick_scalar(sources, "phone")[0],
        "addresses": None,
        "external_ids": merge_external_ids(sources),
        "updated_at": max(sources, key=lambda s: parse_ts(s["updated_at"]))["updated_at"],
    }

    provenance = {
        "customer_id": "CRM" if canonical_id == crm.get("customer_id") else "ERP",
        "first_name": pick_scalar(sources, "first_name")[1],
        "last_name": pick_scalar(sources, "last_name")[1],
        "email": pick_scalar(sources, "email")[1],
        "phone": pick_scalar(sources, "phone")[1],
        "addresses": {},
        "external_ids": "union(CRM,ERP)",
        "updated_at": max(sources, key=lambda s: parse_ts(s["updated_at"]))["system"],
    }

    addresses, addr_prov = merge_addresses(sources)
    golden["addresses"] = addresses
    provenance["addresses"] = addr_prov

    print("=== GOLDEN RECORD (MDM merge) ===")
    print(json.dumps(golden, indent=2, ensure_ascii=False))
    print("\n=== SOURCE OF TRUTH (per field) ===")
    print(json.dumps(provenance, indent=2, ensure_ascii=False))

    with open("golden_record.json", "w", encoding="utf-8") as f:
        json.dump(golden, f, indent=2, ensure_ascii=False)
    print("\n[INFO] golden_record.json written.")


if __name__ == "__main__":
    main()