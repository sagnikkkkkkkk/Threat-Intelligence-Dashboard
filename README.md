# Threat Intelligence Dashboard — Prototype

A demo dashboard (Streamlit + Plotly + Folium) that visualizes **synthetic**
regional activity data with an interactive map, KPI cards, activity trends,
threat-level distribution, a simulated alert feed, and a template-generated
"AI intelligence report."

> ⚠️ **All data is synthetically generated** (`data_simulator.py`). This
> project does not connect to any real satellite imagery, sensor network,
> or classified intelligence source — it's built for internship/portfolio
> demonstration of a full-stack AI dashboard.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## What's here (Phase 1)

- `app.py` — Streamlit dashboard: map, KPIs, trend chart, distribution
  chart, alert feed, AI-report panel, sidebar filters.
- `data_simulator.py` — generates all synthetic data: region snapshots,
  30-day activity trends, alerts, model performance metrics, and a
  template-based text report.

## Suggested next phases

1. **Backend (FastAPI + PostgreSQL)**
   - Move data generation behind a FastAPI service with REST endpoints
     (`/regions`, `/alerts`, `/trends`, `/models`).
   - Persist snapshots to PostgreSQL instead of in-memory generation.
   - Have the Streamlit app call the API instead of importing the
     simulator directly.

2. **Real (non-classified) data sources**, if in scope:
   - Open satellite imagery: Sentinel-2 via Copernicus Open Access Hub,
     or NASA Worldview — both free and unclassified.
   - Public conflict/event datasets (e.g. ACLED) for realistic activity
     trend shapes, used only for pattern/format reference in a student
     project context.

3. **ML models** (swap in for the current stubs)
   - **Isolation Forest** on activity-score time series → anomaly flags
     feeding the alert feed.
   - **LSTM** for activity-trend forecasting (replace the linear trend
     mock in `generate_activity_trend`).
   - **XGBoost / Random Forest** for threat-level classification from
     engineered features (activity score, rate of change, historical
     volatility).
   - **YOLOv8** for object detection on sample/public satellite crops
     (vehicles, structures) — useful as a CV demo on openly licensed
     imagery.
   - **BERT** for classifying/summarizing open-source text reports
     (news wire style synthetic text) feeding the "AI report" panel.

4. **Polish**
   - Auth (even basic) if this ever handles anything sensitive.
   - Historical playback slider on the map.
   - Export report as PDF (see PDF generation tooling).

## Project structure

```
military_dashboard/
├── app.py              # Streamlit UI
├── data_simulator.py   # synthetic data + mock "AI report" generator
├── requirements.txt
└── README.md
```
