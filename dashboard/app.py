import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://app:8000")

st.set_page_config(page_title="CryptoBot - Tableau de bord", layout="wide")
st.title("CryptoBot - Tableau de bord")

# Selecteurs
col_sel1, col_sel2, col_sel3 = st.columns(3)
symbol = col_sel1.selectbox("Crypto", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"], index=0)
interval = col_sel2.selectbox("Intervalle", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3)
period = col_sel3.selectbox("Periode", ["1D", "1W", "1M", "1Y"], index=0)


def fetch_json(url: str, params: dict) -> dict | list | None:
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        st.error("API CryptoBot indisponible.")
        return None


params = {"symbol": symbol, "interval": interval, "period": period}

# Stats
stats = fetch_json(f"{API_URL}/stats", params)
if stats is None:
    st.stop()

st.subheader("Vue du marche")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Dernier prix", f"{stats.get('last_price', 'N/A')}")
col2.metric("Prix maximum", f"{stats.get('max_price', 'N/A')}")
col3.metric("Prix minimum", f"{stats.get('min_price', 'N/A')}")
col4.metric("Volume moyen", f"{stats.get('avg_volume', 'N/A')}")

st.divider()

# Signal
signal_data = fetch_json(f"{API_URL}/signals", params)
if signal_data is None:
    st.stop()

signal_value = signal_data.get("signal", "N/A")
decision_map = {
    "BUY": "ACHAT (BUY)",
    "HOLD": "ATTENTE (HOLD)",
    "SELL": "VENTE (SELL)",
}
decision_text = decision_map.get(signal_value, "Inconnue")

st.subheader("Signal CryptoBot")
st.markdown(f"**Signal : {signal_value}**")
st.markdown(f"**Decision : {decision_text}**")
st.write(f"Prix : {signal_data.get('close', 'N/A')}")
st.write(f"EMA 20 : {signal_data.get('ema_20', 'N/A')}")
st.write(f"RSI 14 : {signal_data.get('rsi', 'N/A')}")
st.write(f"Explication : {signal_data.get('reason', 'N/A')}")
st.caption("Signal experimental a vocation pedagogique. Il ne constitue pas un conseil financier.")

st.divider()

# Graphique
chart_data = fetch_json(f"{API_URL}/charts", params)
if chart_data is None:
    st.stop()

if isinstance(chart_data, dict):
    chart_data = [chart_data]

df = pd.DataFrame(chart_data)

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.subheader("Graphique")
if {"date", "close", "ema_20"}.issubset(df.columns):
    df_long = df[["date", "close", "ema_20"]].melt(id_vars="date", var_name="serie", value_name="valeur")
    fig = px.line(df_long, x="date", y="valeur", color="serie", title="Evolution du prix et EMA 20")
    st.plotly_chart(fig, width="stretch")
else:
    st.warning("Donnees de graphique incompletes.")

st.subheader("Donnees recentes")
st.dataframe(df.tail(30), width="stretch")
