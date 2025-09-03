# app/streamlit_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from src.processing import load_data, preprocess, detect_hotspots_dbscan, aggregate_time_patterns, export_hotspot_summary
from src.visualization import plot_hotspots_map

st.set_page_config(page_title="VelociCity", layout="wide")

st.title("🚦 VelociCity 🚦")

# Upload dataset
uploaded_file = st.file_uploader("Upload CSV traffic dataset", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.success("Dataset loaded successfully!")
else:
    st.info("Using sample dataset.")
    df = load_data("data/sample_traffic.csv")

# Preprocess
df = preprocess(df)

# Sidebar: DBSCAN parameters
st.sidebar.header("DBSCAN Clustering Parameters")
eps = st.sidebar.slider("Epsilon (degrees)", 0.0005, 0.01, 0.001, 0.0005)
min_samples = st.sidebar.slider("Min Samples", 3, 20, 5)

# Detect hotspots
df = detect_hotspots_dbscan(df, eps=eps, min_samples=min_samples)
st.subheader("Hotspot Map")
fmap = plot_hotspots_map(df)
st_folium(fmap, width=700, height=500)

# Show patterns
st.subheader("Time Patterns")
hourly, weekday = aggregate_time_patterns(df)
st.bar_chart(hourly.set_index('hour'))
st.bar_chart(weekday.set_index('weekday'))

# Export summary
if st.button("Export Hotspot Summary"):
    summary = export_hotspot_summary(df)
    summary.to_csv("hotspot_summary.csv", index=False)
    st.success("Hotspot summary exported as hotspot_summary.csv")
