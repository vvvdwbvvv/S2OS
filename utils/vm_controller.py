import subprocess
import time
import os

def run_vm_and_check(kernel_path, image_path, log_path, keyword="EXPLOIT_SUCCESS", timeout=10):
    if not os.path.isfile(kernel_path):
        raise FileNotFoundError(f"Kernel image not found: {kernel_path}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Rootfs image not found: {image_path}")

    if os.path.exists(log_path):
        os.remove(log_path)

    proc = subprocess.Popen([
        "qemu-system-x86_64",
        "-kernel", kernel_path,
        "-drive", f"file={image_path},format=raw,if=virtio",
        "-append", "root=/dev/vda console=ttyS0",
        "-nographic",
        "-virtfs", "local,path=./vm,mount_tag=host0,security_model=none",
        "-serial", f"file:{log_path}"
    ])

    try:
        for _ in range(timeout):
            if os.path.exists(log_path):
                with open(log_path) as f:
                    content = f.read()
                    if keyword in content:
                        proc.terminate()
                        return True
            time.sleep(1)
    finally:
        proc.terminate()

    return False


def run_vagrant_and_check(*, log_path, **kwargs):
    subprocess.run(["vagrant", "ssh", "-c", "bash /vagrant/start_vm.sh"], timeout=15)

    with open("vm/serial.log", "r") as f:
        log = f.read()
        return any(keyword in log for keyword in ["Segmentation fault", "pwned", "uid=0"])

