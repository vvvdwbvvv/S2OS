# utils/scan_manager.py
import nmap
import time
from utils.history_manager import record_event

def run_scan(vm_ip, ports="1-65535", scan_args="-sV"):
    """
    使用 nmap 掃描指定 VM IP，找出開放埠與 service banner，
    並記錄一條 'detected' 事件，detail 裡帶上 port list。
    """
    nm = nmap.PortScanner()
    start = time.time()
    nm.scan(vm_ip, ports, arguments=scan_args)
    elapsed = time.time() - start

    open_ports = []
    for proto in nm[vm_ip].all_protocols():
        for port in nm[vm_ip][proto].keys():
            info = nm[vm_ip][proto][port]
            open_ports.append({
                "port": port,
                "proto": proto,
                "service": info.get("name"),
                "banner": info.get("product") + " " + info.get("version", "")
            })

    # 記錄掃描事件
    record_event("detected", detail={
        "vm_ip": vm_ip,
        "elapsed": f"{elapsed:.1f}s",
        "open_ports": open_ports
    })
    return open_ports
