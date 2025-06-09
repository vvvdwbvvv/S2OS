# app.py
import streamlit as st
import ctypes
from utils.fake_server import clear_serial_log, run_fake_defense
from utils.plugin_loader import load_plugins
from utils.vm_controller import run_vm_and_check
from utils.defense_config import render_defense_config
from utils.history_manager import clear_event_log, record_attack, load_history
from utils.visualizer import plot_success_rate
from utils.history_manager import initialize_history_file
from utils.attack_manager import run_attack
from utils.vm_controller import run_defense
from utils.history_manager import load_events
import time

clear_serial_log()
clear_event_log()
SERIAL_LOG = "serial.log"

def append_serial_log(msg):
    with open(SERIAL_LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} [UI] {msg}\n")

for level in ["success", "info", "error", "warning", "write"]:
    orig = getattr(st, level)
    def wrapper(msg, level=level, orig=orig, **kwargs):
        append_serial_log(msg)
        return orig(msg, **kwargs)
    setattr(st, level, wrapper)

st.set_page_config(page_title="S2OS", layout="wide")
st.title("SimSecureOS - 攻擊模擬平台")

# 載入 plugin
plugins = load_plugins()
initialize_history_file()

# 防禦設定視覺化
st.sidebar.header("防禦機制設定")
defense_config = render_defense_config()

# 架構過濾 + 多選
arch_filter = st.sidebar.selectbox(
    "選擇目標架構",
    ["All"] + sorted(list(set(p["arch"] for p in plugins)))
)
filtered_plugins = [p for p in plugins if arch_filter == "All" or p["arch"] == arch_filter]
selected_plugins = st.multiselect(
    "選擇攻擊模組",
    filtered_plugins,
    format_func=lambda p: f"{p['name']} ({p.get('cve', 'N/A')})"
)

if st.button("🚀 發動攻擊") and selected_plugins:
    for plugin in selected_plugins:
        success = run_attack(plugin, defense_config)
        st.success("✅ Exploit 成功" if success else "❌ Exploit 失敗")

defense_choices = st.sidebar.multiselect(
    "Select Defense Actions",
    ["Patch vsftpd", "Close port 21", "Revert snapshot"]
)

if st.sidebar.button("🛡️ 執行防禦"):
    for choice in defense_choices:
        msg = run_fake_defense(choice, defense_config)
        st.sidebar.text(msg)

st.subheader("Serial Log")
try:
    with open("serial.log") as f:
        log = f.read()
    st.code(log, language="bash")
except FileNotFoundError:
    st.info("=No Serial log found")

st.subheader("事件序列")
events = load_events()
st.json(events)

# 歷史記錄顯示
st.subheader("攻擊歷史紀錄")
df = load_history()
st.dataframe(df, use_container_width=True)

# 成功率圖表
st.subheader("成功率分析")
st.plotly_chart(plot_success_rate(df), use_container_width=True)
