import streamlit as st

from keyworld import KEYWORDS
from sources import SOURCES

st.set_page_config(
    page_title="Agent Emploi Défense",
    layout="wide"
)

st.title("🚀 Agent Emploi Défense / Cyber / IA")

st.write(
    "Dashboard de veille automatisée pour les offres Défense, Cybersécurité, Data et Intelligence Artificielle."
)

# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Sources surveillées",
    len(SOURCES)
)

col2.metric(
    "Sources automatiques",
    len([s for s in SOURCES if s["mode"] == "scraping"])
)

col3.metric(
    "Sources manuelles",
    len([s for s in SOURCES if s["mode"] == "manual"])
)

st.divider()

# Sources

st.subheader("📡 Sources surveillées")

for source in SOURCES:

    with st.expander(source["name"]):

        st.write(f"Type : {source['type']}")
        st.write(f"Mode : {source['mode']}")
        st.write(f"URL : {source['url']}")

st.divider()

# Mots clés

st.subheader("🔎 Mots-clés surveillés")

for keyword in KEYWORDS:

    st.write(f"✅ {keyword}")
    