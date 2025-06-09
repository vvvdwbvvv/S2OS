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
    try:
        subprocess.run([
            "docker", "run", "--rm", 
            "tonistiigi/binfmt", "--install", "all"
        ], check=True)
    except subprocess.CalledProcessError as e:
        # Mac 上會失敗，可以跳過
        record_event("warning", detail={"msg": "binfmt install failed, skipping", "error": str(e)})
   
