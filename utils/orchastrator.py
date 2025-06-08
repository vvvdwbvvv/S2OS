# utils/orchestrator.py
import os
import subprocess
import time
import ctypes


def run_full_attack(plugin: dict, defense_config: dict) -> tuple[bool, str]:
    """
    Args:
      plugin: dict, 
          - so_path: 
          - entry_function: 
          - arch: 
          - kernel_path, image_path 
          - success_log: VM 內成功關鍵字
      defense_config: dict 

    Returns:
      success: bool, 
      log: str, 
    """
    # 1. Pre-check: SO file
    so_path = plugin.get('so_path')
    if not so_path or not os.path.isfile(so_path):
        return False, f"[Orch] Cannot find plugin.so: {so_path}"

    # 2. 取 kernel/image 路徑
    kernel = plugin.get('kernel_path', 'vm/buildroot-2024.02/output/images/bzImage')
    image = plugin.get('image_path', 'vm/buildroot-2024.02/output/images/rootfs.ext2')
    for path in (kernel, image):
        if not os.path.isfile(path):
            return False, f"[Orch] Cannot find image file: {path}"

    # remove old log
    log_path = plugin.get('log_path', 'vm/serial.log')
    if os.path.exists(log_path):
        os.remove(log_path)

    arch = plugin.get('arch', 'x86_64')
    success_keyword = plugin.get('success_log', 'EXPLOIT_SUCCESS')

    # 3. launch VM
    if arch == 'x86_64':
        cmd = [
            'qemu-system-x86_64',
            '-kernel', kernel,
            '-drive', f'file={image},format=raw,if=virtio',
            '-append', 'root=/dev/vda console=ttyS0',
            '-nographic',
            '-virtfs', 'local,path=./vm,mount_tag=host0,security_model=none',
            '-serial', f'file:{log_path}'
        ]
    elif arch == 'arm64':
        cmd = [
            'qemu-system-aarch64',
            '-machine', 'virt',
            '-cpu', 'cortex-a53',
            '-kernel', kernel,
            '-append', 'root=/dev/vda console=ttyAMA0',
            '-drive', f'file={image},format=raw,if=none,id=hd0',
            '-device', 'virtio-blk-device,drive=hd0',
            '-nographic',
            '-virtfs', 'local,path=./vm,mount_tag=host0,security_model=none',
            '-serial', f'file:{log_path}'
        ]
    else:
        return False, f"[Orch] Unsupported arch: {arch}"

    proc = subprocess.Popen(cmd)

    start = time.time()
    timeout = plugin.get('timeout', 20)
    log = ''
    try:
        while time.time() - start < timeout:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    log = f.read()
                    if success_keyword in log:
                        break
            time.sleep(1)
    finally:
        proc.terminate()

    # 4. log and exe exploit
    try:
        lib = ctypes.CDLL(so_path)
        entry = getattr(lib, plugin.get('entry_function', 'run_exploit'))
        entry()
    except Exception as e:
        log += f"\n[Orch] Exe. exploit: {e}"
        return False, log

    success = success_keyword in log
    return success, log
