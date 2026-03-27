"""
sync_comparison.py
Applies the same updates in two modes:
1) REAL-TIME: apply immediately; log each event
2) BATCH: accumulate as JSONL; process later; log results
Writes: realtime.log, batch_updates.jsonl, batch.log
"""

import json
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


def iso_now():
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def apply_update(record: dict, event: dict) -> dict:
    op = event["op"]
    if op == "update":
        record[event["path"]] = event["value"]
    elif op == "add_address":
        new_addr = event["value"]
        by_type = {a.get("type"): i for i, a in enumerate(record.get("addresses", []))}
        if new_addr.get("type") in by_type:
            record["addresses"][by_type[new_addr["type"]]] = new_addr
        else:
            record.setdefault("addresses", []).append(new_addr)
    record["updated_at"] = event["ts"]
    return record


def load_golden_fallback():
    return {
        "customer_id": "CUST-1001",
        "first_name": "Amina",
        "last_name": "Rahman",
        "email": "mina.rahman@example.com",
        "phone": "+1-416-555-0197",
        "addresses": [
            {"type": "home", "line1": "123 Bloor St W", "city": "Toronto", "province": "ON", "postal_code": "M5S 1W7", "country": "CA"},
            {"type": "billing", "line1": "400 King St E", "city": "Toronto", "province": "ON", "postal_code": "M5A 1L7", "country": "CA"},
        ],
        "external_ids": {"crm": "CUST-1001", "erp": "1001"},
        "updated_at": "2026-02-12T08:30:00Z",
    }


def main():
    gp = Path("golden_record.json")
    if gp.exists():
        with open(gp, "r", encoding="utf-8") as f:
            golden = json.load(f)
        print("[INFO] Loaded golden record from golden_record.json")
    else:
        golden = load_golden_fallback()
        print("[INFO] golden_record.json not found; using fallback in script.")

    events = [
        {"ts": "2026-02-13T12:00:00Z", "op": "update", "path": "email", "value": "amina.new@example.com"},
        {"ts": "2026-02-13T12:01:15Z", "op": "add_address", "value": {"type": "shipping", "line1": "77 Dundas St W", "city": "Toronto", "province": "ON", "postal_code": "M5G 1Z3", "country": "CA"}},
        {"ts": "2026-02-13T12:03:42Z", "op": "update", "path": "phone", "value": "+1-416-555-7777"},
    ]

    # REAL-TIME
    rt_state = deepcopy(golden)
    rt_log_lines = []
    print("=== REAL-TIME UPDATES ===")
    for e in events:
        before = deepcopy(rt_state)
        rt_state = apply_update(rt_state, e)
        line = f"[REALTIME] applied {e['op']} at {e['ts']} | before→after: {json.dumps(before, ensure_ascii=False)} → {json.dumps(rt_state, ensure_ascii=False)}"
        rt_log_lines.append(line)
        print(line)
        time.sleep(0.2)

    with open("realtime.log", "w", encoding="utf-8") as f:
        f.write("\n".join(rt_log_lines))
    print("[INFO] realtime.log written.")

    # BATCH
    with open("batch_updates.jsonl", "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    print("=== BATCH PROCESSING ===")
    print(f"[BATCH] job_start={iso_now()} reading batch_updates.jsonl")
    time.sleep(0.5)

    batch_state = deepcopy(golden)
    batch_log_lines = []
    with open("batch_updates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            before = deepcopy(batch_state)
            batch_state = apply_update(batch_state, e)
            log_line = f"[BATCH] applied {e['op']} (event_ts={e['ts']}) | before→after: {json.dumps(before, ensure_ascii=False)} → {json.dumps(batch_state, ensure_ascii=False)}"
            batch_log_lines.append(log_line)
            print(log_line)

    print(f"[BATCH] job_end={iso_now()} final_state={json.dumps(batch_state, ensure_ascii=False)}")
    with open("batch.log", "w", encoding="utf-8") as f:
        f.write("\n".join(batch_log_lines))
    print("[INFO] batch.log written. batch_updates.jsonl written.")


if __name__ == "__main__":
    main()