# utils/scan_manager.py
import nmap
from utils.history_manager import record_event

def run_scan(vm_ip="127.0.0.1", ports="1-65535", scan_args="-sV"):
    """
    掃描 localhost:2222,80 … map 到 container 的埠
    """
    nm = nmap.PortScanner()
    nm.scan(vm_ip, ports, arguments=scan_args)
    open_ports = []
    for proto in nm[vm_ip].all_protocols():
        for port in nm[vm_ip][proto].keys():
            info = nm[vm_ip][proto][port]
            open_ports.append({
                "port": port,
                "proto": proto,
                "service": info.get("name"),
                "banner": f"{info.get('product','')} {info.get('version','')}".strip()
            })
    record_event("detected", detail={"open_ports": open_ports})
    return open_ports
