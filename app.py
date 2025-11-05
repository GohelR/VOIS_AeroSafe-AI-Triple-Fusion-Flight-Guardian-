import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import pydeck as pdk
import time

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="AeroSafe AI Dashboard", layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    csv_url = "https://raw.githubusercontent.com/GohelR/VOIS_AeroSafe-AI-Triple-Fusion-Flight-Guardian-/main/data/fused_risk_sample.csv"
    return pd.read_csv(url)

df = load_data()

# ---------- HEADER ----------
st.title("✈️ AeroSafe AI – Triple Fusion Flight Guardian")
st.markdown("### Real-time risk monitoring using Aircraft, Weather, and Pilot analytics")

# ---------- LOTTIE ANIMATION ----------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"  # airplane animation
st_lottie(load_lottieurl(lottie_url), height=180, key="airplane")

# ---------- SENSOR STATUS ----------
st.subheader("⚙️ Sensor Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.success("Engine 1 Temp: Online")
    st.success("Engine 2 Temp: Online")

with col2:
    st.warning("Navigation System: Warning ⚠️")
    st.success("APU: Online")

with col3:
    st.error("Landing Gear: Offline")
    st.success("Hydraulic Pressure: Online")

# ---------- FLIGHT RISK GRAPH ----------
st.subheader("📈 Risk Score Trend")
st.line_chart(df["risk_score"])

# ---------- MAP VIEW (Simulated) ----------
st.subheader("🗺️ Live Flight Path (Simulation)")
view_state = pdk.ViewState(latitude=23.0, longitude=72.6, zoom=5, pitch=0)
path = [
    {"lat": 23.0, "lon": 72.6},
    {"lat": 23.5, "lon": 73.1},
    {"lat": 24.0, "lon": 74.0},
    {"lat": 24.5, "lon": 75.0},
]
layer = pdk.Layer("PathLayer", path, get_path="[['lon', 'lat']]", get_color=[255, 0, 0], width_scale=10)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", layers=[layer], initial_view_state=view_state))

# ---------- PILOT STATUS ----------
st.subheader("👨‍✈️ Pilot Health Monitor")
latest = df.tail(1).iloc[0]
colA, colB, colC = st.columns(3)
colA.metric("Heart Rate", f"{latest['heart_rate_bpm']} bpm")
colB.metric("Fatigue Score", latest['fatigue_score'])
colC.metric("Overall Risk", f"{round(latest['risk_score']*100,1)} %")

# ---------- AI MESSAGE ----------
st.subheader("💬 AI Copilot Insight")
if latest['risk_score'] > 0.7:
    st.error("⚠️ High risk detected! Possible engine or weather anomaly.")
elif latest['risk_score'] > 0.4:
    st.warning("🟡 Moderate risk detected. Monitor pilot condition & environment.")
else:
    st.success("🟢 All systems normal. Safe flight conditions.")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Developed by Team 58 – VOIS Innovation Marathon 2.0 | Mentor: Mr. Vignesh Mathiyalagan")
