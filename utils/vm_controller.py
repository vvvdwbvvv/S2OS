import subprocess
import time
import os

def run_vm_and_check(image_path, log_path, keyword="EXPLOIT_SUCCESS", timeout=10):
    if os.path.exists(log_path):
        os.remove(log_path)
    proc = subprocess.Popen([
        "qemu-system-x86_64", "-hda", image_path, "-m", "512M", "-nographic", "-serial", f"file:{log_path}"
    ])
    for _ in range(timeout):
        if os.path.exists(log_path):
            with open(log_path) as f:
                if keyword in f.read():
                    proc.terminate()
                    return True
        time.sleep(1)
    proc.terminate()
    return False