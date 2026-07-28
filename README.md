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

### Option A — Frontend only (no backend/database needed)

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app auto-detects whether the API is running. If it isn't, it falls
back to the in-process synthetic generator — so this still works standalone.

### Option B — Full stack (FastAPI + PostgreSQL + Streamlit)

1. **Start PostgreSQL** and create a database (defaults below, override via env vars):
   ```bash
   createdb threat_dashboard   # or: psql -c "CREATE DATABASE threat_dashboard;"
   ```

2. **Install backend deps and seed the database**:
   ```bash
   pip install -r requirements.txt
   cd backend
   export POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres \
          POSTGRES_HOST=localhost POSTGRES_PORT=5432 POSTGRES_DB=threat_dashboard
   python seed.py
   ```

3. **Run the API**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   Interactive docs: http://localhost:8000/docs

4. **Run the dashboard** (in a separate terminal, from the project root):
   ```bash
   export API_BASE_URL=http://localhost:8000   # optional, this is the default
   streamlit run app.py
   ```
   The sidebar will show "🟢 FastAPI + PostgreSQL" once connected.

## What's here (Phase 1 + 2)

**Frontend**
- `app.py` — Streamlit dashboard: map, KPIs, trend chart, distribution
  chart, alert feed, AI-report panel, sidebar filters. Uses the API when
  available, otherwise falls back to local synthetic generation.
- `data_simulator.py` — generates synthetic data (used for local fallback
  and to seed the database): region snapshots, 30-day activity trends,
  alerts, model performance metrics, and a template-based text report.
- `api_client.py` — thin `requests`-based client the dashboard uses to
  call the FastAPI backend.

**Backend**
- `backend/main.py` — FastAPI app exposing `/regions`, `/trends`,
  `/alerts`, `/models`, `/report`.
- `backend/models.py` — SQLAlchemy ORM models (`Region`, `RegionSnapshot`,
  `ActivityTrendPoint`, `Alert`, `ModelScore`).
- `backend/schemas.py` — Pydantic response schemas.
- `backend/database.py` — engine/session setup, reads connection info
  from `POSTGRES_*` environment variables.
- `backend/seed.py` — creates tables and populates them with synthetic
  data (re-run any time to reset/refresh the dataset).

## Suggested next phases

1. **Real (non-classified) data sources**, if in scope:
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
├── api_client.py       # HTTP client -> FastAPI backend (with local fallback)
├── data_simulator.py   # synthetic data + mock "AI report" generator
├── requirements.txt
├── README.md
└── backend/
    ├── main.py          # FastAPI app / REST endpoints
    ├── models.py        # SQLAlchemy ORM models
    ├── schemas.py        # Pydantic response schemas
    ├── database.py       # DB engine/session (reads POSTGRES_* env vars)
    └── seed.py            # populates PostgreSQL with synthetic data
```
