# utils/attack_manager.py
import ctypes
import subprocess
import os
import time
from utils.history_manager import record_event
from utils.scan_manager import run_scan

def run_attack(plugin, vm_paths, defense_config):
    """
    執行單一攻擊 plugin，並且記錄 'exposed','detected','exploited' 三種事件。
    返回最後的 success(bool)。
    """
    so_path = plugin["so_path"]
    name = plugin["name"]
    # 1. 標記「已暴露漏洞」
    record_event("vm_started", detail={"kernel": vm_paths["kernel"], "image": vm_paths["rootfs"]})
    # 這裡假設 VM 用 hostfwd map 到 localhost:2222 SSH 或 http
    time.sleep(15)  # 等待 VM 完全 boot

    vm_ip = "127.0.0.1"    
    vm_ssh_port = 2222       
    ports = "1-1024"        
    open_ports = run_scan(vm_ip, ports=ports)

    # 3. 記錄「已暴露漏洞」
    record_event("exposed", detail={"plugin": plugin["name"], "open_ports": open_ports})

    try:
        lib = ctypes.CDLL(so_path)
        lib.run_exploit()
    except OSError:
        # fallback: 如果 .so 載入失敗，可以改用 subprocess 執行可執行檔
        bin_path = plugin.get("bin_path")
        if not bin_path or not os.path.exists(bin_path):
            raise
        subprocess.run([bin_path], check=True)

    # 3. 標記「已檢測到漏洞」（不論是否攻擊成功）
    record_event("detected", detail={"plugin": name})

    # 4. 檢測實際影響（透過 vm_controller 取得結果）
    from utils.vm_controller import run_vm_and_check
    success = run_vm_and_check(
        kernel_path=vm_paths["kernel"],
        image_path=vm_paths["rootfs"],
        log_path=vm_paths["serial_log"]
    )

    # 5. 標記最終結果
    record_event("exploited" if success else "exploit_failed",
                 detail={"plugin": name})
    return success
