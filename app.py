"""
app.py
------
AI-Based Intelligence & Threat Analysis Dashboard — DEMO / PROTOTYPE
All data on this dashboard is synthetically generated (see data_simulator.py)
for portfolio / internship demonstration purposes. It does not represent
real intelligence, imagery, or operational data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from data_simulator import (
    THREAT_COLORS,
    generate_region_snapshot,
    generate_activity_trend,
    generate_alerts,
    generate_model_scores,
    generate_ai_report,
)

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Threat Intelligence Dashboard (Demo)",
    page_icon="🛰️",
    layout="wide",
)

# ----------------------------------------------------------------------
# Cached synthetic data (regenerated on manual refresh)
# ----------------------------------------------------------------------
@st.cache_data(ttl=300)
def load_data():
    regions = generate_region_snapshot()
    trend = generate_activity_trend()
    alerts = generate_alerts()
    models = generate_model_scores()
    return regions, trend, alerts, models


st.markdown(
    """
    <style>
    .demo-banner {
        background-color: #1f2933;
        color: #f1c40f;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-bottom: 12px;
        border: 1px solid #f1c40f33;
    }
    </style>
    <div class="demo-banner">
    ⚠️ DEMO MODE — all data below is synthetically generated for prototype
    purposes only. No real intelligence or operational sources are used.
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("🛰️ AI-Based Threat Intelligence Dashboard")
st.caption("Prototype build · Streamlit + Plotly + Folium · Synthetic data")

regions_df, trend_df, alerts_df, models_df = load_data()

# ----------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    if st.button("🔄 Refresh synthetic data"):
        st.cache_data.clear()
        st.rerun()

    selected_regions = st.multiselect(
        "Regions", options=regions_df["region"].tolist(), default=regions_df["region"].tolist()
    )
    selected_levels = st.multiselect(
        "Threat levels",
        options=list(THREAT_COLORS.keys()),
        default=list(THREAT_COLORS.keys()),
    )
    st.divider()
    st.subheader("AI Models Active")
    for _, row in models_df.iterrows():
        st.caption(f"**{row['model']}** — {row['task']} (acc {row['accuracy']*100:.0f}%)")

filtered = regions_df[
    regions_df["region"].isin(selected_regions)
    & regions_df["threat_level"].isin(selected_levels)
]
filtered_alerts = alerts_df[alerts_df["region"].isin(selected_regions)]

# ----------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Monitored Regions", len(filtered))
k2.metric("Active Alerts", len(filtered_alerts))
high_severe = filtered["threat_level"].isin(["High", "Severe"]).sum()
k3.metric("High/Severe Regions", int(high_severe))
avg_conf = filtered["confidence"].mean() if len(filtered) else 0
k4.metric("Avg. Model Confidence", f"{avg_conf*100:.0f}%")

st.divider()

# ----------------------------------------------------------------------
# Map + region table
# ----------------------------------------------------------------------
map_col, table_col = st.columns([2, 1])

with map_col:
    st.subheader("🌍 Interactive Threat Map")
    m = folium.Map(location=[22, 80], zoom_start=4, tiles="CartoDB dark_matter")
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8 + row["activity_score"] / 12,
            color=THREAT_COLORS[row["threat_level"]],
            fill=True,
            fill_color=THREAT_COLORS[row["threat_level"]],
            fill_opacity=0.75,
            popup=folium.Popup(
                f"<b>{row['region']}</b><br>"
                f"Threat level: {row['threat_level']}<br>"
                f"Activity score: {row['activity_score']}<br>"
                f"Confidence: {row['confidence']*100:.0f}%",
                max_width=250,
            ),
            tooltip=row["region"],
        ).add_to(m)
    st_folium(m, use_container_width=True, height=460)

with table_col:
    st.subheader("📍 Region Snapshot")
    display_df = filtered[["region", "threat_level", "activity_score", "confidence"]].copy()
    display_df["confidence"] = (display_df["confidence"] * 100).round(0).astype(int).astype(str) + "%"
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=420)

st.divider()

# ----------------------------------------------------------------------
# Trends
# ----------------------------------------------------------------------
st.subheader("📈 Military Activity Trends (30-day, simulated)")
trend_filtered = trend_df[trend_df["region"].isin(selected_regions)]
fig_trend = px.line(
    trend_filtered,
    x="date",
    y="activity_score",
    color="region",
    labels={"activity_score": "Activity Score", "date": "Date"},
)
fig_trend.update_layout(height=380, legend=dict(orientation="h", y=-0.25))
st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------------------------------------------------
# Threat level distribution + model performance
# ----------------------------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Threat Level Distribution")
    dist = filtered["threat_level"].value_counts().reindex(THREAT_COLORS.keys()).fillna(0)
    fig_bar = go.Figure(
        go.Bar(
            x=dist.index,
            y=dist.values,
            marker_color=[THREAT_COLORS[l] for l in dist.index],
        )
    )
    fig_bar.update_layout(height=320, yaxis_title="Regions")
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🤖 AI Model Performance")
    fig_models = px.bar(
        models_df,
        x="model",
        y="accuracy",
        color="latency_ms",
        color_continuous_scale="Blues",
        labels={"accuracy": "Accuracy", "latency_ms": "Latency (ms)"},
    )
    fig_models.update_layout(height=320)
    st.plotly_chart(fig_models, use_container_width=True)

st.divider()

# ----------------------------------------------------------------------
# Alerts + AI report
# ----------------------------------------------------------------------
alert_col, report_col = st.columns([1.3, 1])

with alert_col:
    st.subheader("🔔 Alert Feed")
    for _, a in filtered_alerts.head(10).iterrows():
        color = THREAT_COLORS[a["threat_level"]]
        st.markdown(
            f"""
            <div style="border-left:4px solid {color}; padding:6px 10px; margin-bottom:6px; background:#11151c; border-radius:4px;">
            <b>{a['id']}</b> · {a['timestamp'].strftime('%H:%M UTC')} · <span style="color:{color}">{a['threat_level']}</span><br>
            <small>{a['region']}</small><br>
            {a['message']}<br>
            <small style="opacity:0.6;">source model: {a['model_source']}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

with report_col:
    st.subheader("📄 AI-Generated Intelligence Report")
    st.markdown(generate_ai_report(filtered if len(filtered) else regions_df))

st.divider()
st.caption(
    "Prototype dashboard for internship/portfolio use. Data source: synthetic generator "
    "(data_simulator.py). Not connected to any real satellite, sensor, or intelligence feed."
)
