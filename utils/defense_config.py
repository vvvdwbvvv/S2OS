import streamlit as st

def render_defense_config():
    return {
        "aslr": st.sidebar.checkbox("啟用 ASLR", value=True),
        "dep": st.sidebar.checkbox("啟用 DEP", value=True),
        "canary": st.sidebar.checkbox("啟用 Stack Canary", value=False),
    }

