import csv
import os
import pandas as pd
import json
from datetime import datetime

HISTORY_PATH = "../attack_history.csv"
EVENT_LOG = "events.jsonl"

def initialize_history_file():
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "plugin", "cve", "success", "aslr", "dep", "canary"])
            writer.writeheader()

def record_attack(plugin, success, defense_config):
    row = {
        "timestamp": datetime.now().isoformat(),
        "plugin": plugin["name"],
        "cve": plugin["cve"],
        "success": success,
        **defense_config
    }
    write_header = not os.path.exists(HISTORY_PATH)
    with open(HISTORY_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())   
        if write_header:
            writer.writeheader()
        writer.writerow(row)

def load_history():
    if os.path.exists(HISTORY_PATH) and os.path.getsize(HISTORY_PATH) > 0:
        return pd.read_csv(HISTORY_PATH)
    return pd.DataFrame(columns=["timestamp", "plugin", "cve", "success", "aslr", "dep", "canary"])

def record_event(event_type, detail=None):
    """
    將單場次事件（exposed, detected, exploited, defended...）追加到 events.jsonl
    """
    detail = detail or {}
    entry = {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "event": event_type,
        "detail": detail
    }
    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def load_events():
    """
    讀取本場次的事件列表，返回 List[dict]
    """
    events = []
    if not os.path.exists(EVENT_LOG):
        return events
    with open(EVENT_LOG) as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events