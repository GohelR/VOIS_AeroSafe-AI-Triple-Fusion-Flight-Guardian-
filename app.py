import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import pydeck as pdk

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="AeroSafe AI Dashboard", layout="wide")

# ---------- DATA LOADING ----------
@st.cache_data
def load_data():
    # ✅ make sure this path exists exactly in your GitHub repo
    csv_url = "https://raw.githubusercontent.com/GohelR/VOIS_AeroSafe-AI-Triple-Fusion-Flight-Guardian-/main/data/fused_risk_sample.csv"
    
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error("⚠️ Could not load data from GitHub. Please check file path or repo visibility.")
        st.write(e)
        st.stop()

df = load_data()   # ✅ now variable defined and loaded safely
