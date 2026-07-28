"""
data_simulator.py
------------------
Generates SYNTHETIC data for the demo dashboard.
No real-world intelligence, satellite feeds, or classified sources are used.
Replace the functions in this file with real data connectors when/if this
project moves past the prototype stage (subject to your organization's
data-access and classification policies).
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

THREAT_LEVELS = ["Low", "Guarded", "Elevated", "High", "Severe"]
THREAT_COLORS = {
    "Low": "#2ecc71",
    "Guarded": "#3498db",
    "Elevated": "#f1c40f",
    "High": "#e67e22",
    "Severe": "#e74c3c",
}

# Generic, publicly-known border/region reference points (illustrative only —
# NOT sourced from any intelligence feed).
REGIONS = [
    {"name": "Region A - North Frontier", "lat": 34.0, "lon": 71.0},
    {"name": "Region B - Eastern Corridor", "lat": 24.9, "lon": 91.9},
    {"name": "Region C - Coastal Zone", "lat": 13.1, "lon": 80.3},
    {"name": "Region D - Western Border", "lat": 28.6, "lon": 70.2},
    {"name": "Region E - Southern Strait", "lat": 8.5, "lon": 76.9},
    {"name": "Region F - Highland Pass", "lat": 33.8, "lon": 76.6},
    {"name": "Region G - River Delta", "lat": 22.5, "lon": 88.3},
    {"name": "Region H - Desert Sector", "lat": 26.9, "lon": 70.9},
]


def generate_region_snapshot():
    """Current threat-level snapshot per region (simulated)."""
    rows = []
    for r in REGIONS:
        level = random.choices(
            THREAT_LEVELS, weights=[30, 28, 22, 14, 6], k=1
        )[0]
        rows.append(
            {
                "region": r["name"],
                "lat": r["lat"],
                "lon": r["lon"],
                "threat_level": level,
                "activity_score": round(np.random.uniform(10, 100), 1),
                "confidence": round(np.random.uniform(0.55, 0.98), 2),
                "last_updated": datetime.utcnow()
                - timedelta(minutes=random.randint(1, 240)),
            }
        )
    return pd.DataFrame(rows)


def generate_activity_trend(days=30):
    """Simulated daily activity-score trend per region."""
    records = []
    base_date = datetime.utcnow() - timedelta(days=days)
    for r in REGIONS:
        baseline = np.random.uniform(20, 50)
        for d in range(days):
            date = base_date + timedelta(days=d)
            noise = np.random.normal(0, 6)
            trend = baseline + 0.4 * d * np.random.uniform(-0.5, 1.2)
            score = max(0, min(100, trend + noise))
            records.append(
                {"date": date, "region": r["name"], "activity_score": round(score, 1)}
            )
    return pd.DataFrame(records)


def generate_alerts(n=12):
    """Simulated alert feed."""
    templates = [
        "Unusual troop movement pattern detected via activity-trend anomaly",
        "Increase in vehicle convoy activity above baseline threshold",
        "Communications activity spike flagged by anomaly model",
        "Satellite pass detected new structure at monitored coordinate",
        "Border-crossing sensor activity above 7-day average",
        "Anomalous nighttime thermal signature flagged for review",
    ]
    rows = []
    for i in range(n):
        region = random.choice(REGIONS)
        level = random.choices(THREAT_LEVELS, weights=[15, 25, 30, 20, 10])[0]
        rows.append(
            {
                "id": f"ALT-{1000+i}",
                "timestamp": datetime.utcnow() - timedelta(minutes=random.randint(1, 600)),
                "region": region["name"],
                "message": random.choice(templates),
                "threat_level": level,
                "model_source": random.choice(
                    ["Isolation Forest", "LSTM", "YOLOv8", "XGBoost", "BERT-NLP"]
                ),
            }
        )
    df = pd.DataFrame(rows).sort_values("timestamp", ascending=False)
    return df.reset_index(drop=True)


def generate_model_scores():
    """Simulated model performance metrics for the 'AI Models' panel."""
    return pd.DataFrame(
        [
            {"model": "Random Forest", "task": "Threat classification", "accuracy": 0.91, "latency_ms": 12},
            {"model": "XGBoost", "task": "Risk scoring", "accuracy": 0.93, "latency_ms": 9},
            {"model": "LSTM", "task": "Activity trend forecasting", "accuracy": 0.87, "latency_ms": 45},
            {"model": "Isolation Forest", "task": "Anomaly detection", "accuracy": 0.89, "latency_ms": 7},
            {"model": "BERT", "task": "Report text classification", "accuracy": 0.92, "latency_ms": 120},
            {"model": "YOLOv8", "task": "Imagery object detection", "accuracy": 0.94, "latency_ms": 38},
        ]
    )


def generate_ai_report(region_df: pd.DataFrame) -> str:
    """
    Template-based 'AI-generated' intelligence summary.
    This is a rule-based text generator for the demo — swap in a real
    NLP/LLM call (e.g. a BERT classifier + templated NLG, or an LLM API)
    for production use.
    """
    top = region_df.sort_values("activity_score", ascending=False).iloc[0]
    calm = region_df.sort_values("activity_score").iloc[0]
    severe_count = (region_df["threat_level"].isin(["High", "Severe"])).sum()

    lines = [
        f"**Daily Synthetic Intelligence Summary — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        f"- Monitored regions: {len(region_df)}",
        f"- Regions at High/Severe threat level: {severe_count}",
        f"- Highest activity: **{top['region']}** (score {top['activity_score']}, "
        f"level: {top['threat_level']}, confidence {top['confidence']*100:.0f}%)",
        f"- Lowest activity: **{calm['region']}** (score {calm['activity_score']}, level: {calm['threat_level']})",
        "",
        "This summary is generated from simulated data for demonstration purposes only "
        "and does not reflect real-world intelligence.",
    ]
    return "\n".join(lines)
