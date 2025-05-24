import plotly.express as px

def plot_success_rate(df):
    if df.empty:
        return px.bar(title="尚無資料")
    grouped = df.groupby("plugin")["success"].mean().reset_index()
    return px.bar(grouped, x="plugin", y="success", title="各攻擊模組成功率", labels={"success": "成功率"})
