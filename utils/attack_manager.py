# utils/attack_manager.py
from utils.docker_manager import start_container, stop_container, exec_in_container
from utils.scan_manager import run_scan
from utils.history_manager import record_event
import time
import os

def run_attack(plugin, defense_config):
    """
    1. (Re)啟動 container
    2. 掃描階段 → detected
    3. record exposed
    4. 在 container 裡執行 exploit
    5. 檢查結果 → exploited / exploit_failed
    6. 停掉 container
    """
    start_container()

    # 1. 掃描
    open_ports = run_scan("127.0.0.1", ports="1-1024")
    record_event("exposed", detail={
        "plugin": plugin.get("name"),
        "open_ports": open_ports
    })

    # 2. 準備執行命令（cmd）
    cmd = plugin.get("cmd")
    if not cmd:
        # plugin["so_path"] 指向本地 plugins/<xxx>.so
        rel = plugin["plugin_path"]
        container_path = f"/opt/app/{rel}"
        cmd = ["bash", "-c", f"chmod +x {container_path} && {container_path}"]
        record_event("warning", detail={
            "msg": "自动生成 cmd",
            "auto_cmd": cmd
        })
    # 2. 執行 exploit
    record_event("exploit_start", detail={"plugin": plugin.get("name")})
    # 假設 plugin["cmd"] 是一個 list，像 ["./exploit-bin", "arg1", "..."]
    out = exec_in_container(cmd)
    record_event("exploit_output", detail={"output": out})

    # 3. 檢查是否成功（簡單以 output 裡有 "uid=0" 或 "root@" 為標準）
    success_markers = ["uid=0", "root@", plugin.get("success_log", "EXPLOIT_SUCCESS")]
    success = any(m in out for m in success_markers)
    record_event("exploited" if success else "exploit_failed",
                 detail={"plugin": plugin.get("name")})

    # 7. 停掉容器
    stop_container()
    return success
