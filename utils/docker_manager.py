# utils/docker_manager.py
import subprocess
import time
import os
from utils.history_manager import record_event

IMAGE = "tleemcjr/metasploitable2"
NAME  = "vuln2"

def start_container():
    """如果容器不存在就拉起來，並記錄事件。"""
    # 先嘗試停止／移除同名舊容器
    subprocess.run(["docker", "rm", "-f", NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 啟動一個新的 vulnerables container
    subprocess.run([
        "docker", "run", "-d",
        "--name", NAME,
        "-p", "2222:22",  # SSH
        "-p", "80:80",    # HTTP
        "-v", f"{os.getcwd()}:/opt/app:ro",
        IMAGE
    ], check=True)
    record_event("vm_started", detail={"type":"docker","container":NAME})
    # 容器啟動需要一些時間
    time.sleep(5)

def stop_container():
    """結束並移除容器。"""
    subprocess.run(["docker", "rm", "-f", NAME], check=False)
    record_event("vm_stopped", detail={"container":NAME})

def exec_in_container(cmd):
    """在容器裡執行指令，返回 stdout (text)。"""
    res = subprocess.run(
        ["docker", "exec", NAME] + cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
    )
    return res.stdout + res.stderr

def enable_multiplatform_emulation():
    """
    在宿主机上注册 QEMU 多架构支持，确保可以运行 linux/amd64 容器。
    只需运行一次或在每次启动前执行。
    """
    subprocess.run([
        "docker", "run", "--rm", "--privileged",
        "multiarch/qemu-user-static",
        "--reset", "-p", "yes"
    ], check=True)


def start_container_multiarch():
    """
    启动一个 linux/amd64 平台的 vuln2 容器，使用 QEMU 多架构模拟。
    """
    # 注册 multiarch QEMU 支持
    enable_multiplatform_emulation()
    # 清理旧容器
    subprocess.run(["docker", "rm", "-f", NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 启动新容器
    subprocess.run([
        "docker", "run", "-d",
        "--privileged", 
        "--platform", "linux/amd64",
        "--name", NAME,
        "-p", "2222:22",
        "-p", "80:80",
        "-v", f"{os.getcwd()}:/opt/app:ro",
        IMAGE
    ], check=True)
    record_event("vm_started", detail={"type": "docker/amd64", "container": NAME})
    # 等待容器内服务启动
    time.sleep(5)
