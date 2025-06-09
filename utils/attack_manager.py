# utils/attack_manager.py
from utils.docker_manager import start_container, stop_container, exec_in_container
from utils.scan_manager import run_scan
from utils.history_manager import record_attack
from utils.history_manager import record_event
from utils.orchastrator import run_full_attack


def run_attack(plugin, defense_config):
    """
    1. 使用 orchastrator 在真實 VM 中執行攻擊
    2. 記錄攻擊結果
    """
    # 執行攻擊並獲取結果
    success, log = run_full_attack(plugin, defense_config)
    
    # 記錄攻擊結果
    record_attack(plugin, success, defense_config)
    
    # 記錄詳細日誌
    record_event("attack_result", detail={
        "plugin": plugin.get("name"),
        "success": success,
        "log": log
    })
    
    return success
