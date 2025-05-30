# app.py
import streamlit as st
import ctypes
from utils.plugin_loader import load_plugins
from utils.vm_controller import run_vm_and_check
from utils.defense_config import render_defense_config
from utils.history_manager import record_attack, load_history
from utils.visualizer import plot_success_rate
from utils.history_manager import initialize_history_file

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
        st.write(f"---\n**執行攻擊：** {plugin['name']}")
        try:
            lib = ctypes.CDLL(plugin["so_path"])
            lib.run_exploit()
            with open("vm/serial.log") as f:
                st.text(f.read())
            success = run_vm_and_check(
                kernel_path="vm/buildroot-2024.02/output/images/bzImage",
                image_path="vm/buildroot-2024.02/output/images/rootfs.ext2",
                log_path="vm/serial.log"
            )
            st.success("✅ 成功！" if success else "❌ 攻擊失敗")
            record_attack(plugin, success, defense_config)
        except Exception as e:
            st.error(f"[錯誤] 無法載入 plugin：{plugin['name']}\n{str(e)}")

# 歷史記錄顯示
st.subheader("攻擊歷史紀錄")
df = load_history()
st.dataframe(df, use_container_width=True)

# 成功率圖表
st.subheader("成功率分析")
st.plotly_chart(plot_success_rate(df), use_container_width=True)
