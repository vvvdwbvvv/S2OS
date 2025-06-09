# utils/fake_server.py
import time
import random
from utils.history_manager import record_event, clear_event_log

SERIAL_LOG = "serial.log"

def append_serial_log(msg):
    with open(SERIAL_LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
        

def start_fake_server():
    open(SERIAL_LOG, "w").close()
    clear_event_log()
    append_serial_log("Booting SimSecureOS VM ...")
    time.sleep(0.2)
    append_serial_log("Loading kernel ... [OK]")
    time.sleep(0.2)
    append_serial_log("Initializing network interfaces ... [OK]")
    time.sleep(0.15)
    append_serial_log("Mounting root filesystem ... [OK]")
    time.sleep(0.15)
    append_serial_log("Starting sshd ... [OK]")
    time.sleep(0.1)
    append_serial_log("Starting httpd ... [OK]")
    time.sleep(0.1)
    append_serial_log("System boot completed. Login: root")
    record_event("vm_started", detail={"type": "fake"})
    return True

def scan_fake_server(plugin=None):
    if plugin and plugin.get("target_ports"):
        all_ports = plugin["target_ports"]
    else:
        all_ports = [22, 80, 443, 3306]

    min_port = 0
    max_port = len(all_ports)
    hit_count = random.randint(min_port, max_port)
    open_ports = sorted(random.sample(all_ports, hit_count)) if hit_count > 0 else []

    for port in all_ports:
        time.sleep(0.05)
        if port in open_ports:
            append_serial_log(f"Port {port}/tcp is open")
        else:
            append_serial_log(f"Port {port}/tcp is closed")

    if open_ports:
        append_serial_log(f"found port：{open_ports}")
    else:
        append_serial_log("found no open ports")

    detail = {
        "plugin": plugin.get("name") if plugin else None,
        "open_ports": open_ports
    }
    record_event("exposed", detail=detail)
    return open_ports

def exec_fake_exploit(plugin):
    name = plugin.get("name", "unknown")
    delay = float(plugin.get("fake_delay", 0.1))
    time.sleep(delay * random.uniform(0.7, 1.4))

    append_serial_log(f"activate：{name}")
    success_rate = float(plugin.get("fake_success_rate", 0.8)) 
    is_success = random.random() < success_rate
    out = plugin.get("fake_output", "EXPLOIT_SUCCESS") if is_success else plugin.get("fake_error", "EXPLOIT_FAILED: Not Vulnerable")
    time.sleep(0.08)

    if is_success:
        append_serial_log(f"[EXPLOIT SUCCESS] {name}: {out}")
    else:
        append_serial_log(f"[EXPLOIT FAIL] {name}: {out}")

    record_event("exploit_start", detail={"plugin": name})
    record_event("exploit_output", detail={"output": out})
    record_event("exploited" if is_success else "exploit_failed", detail={"plugin": name, "success": is_success, "output": out})

    return is_success

def stop_fake_server():
    append_serial_log("System shutdown in progress ...")
    time.sleep(0.1)
    append_serial_log("All services stopped.")
    record_event("vm_stopped", detail={})
    return True
