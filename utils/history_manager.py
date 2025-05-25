import csv
import os
import pandas as pd
from datetime import datetime

HISTORY_PATH = "../attack_history.csv"

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
