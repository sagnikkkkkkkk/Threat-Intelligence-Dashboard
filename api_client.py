"""
api_client.py
-------------
Thin HTTP client the Streamlit app uses to talk to the FastAPI backend.
Falls back to the in-process synthetic generator (data_simulator.py) if
the API is unreachable, so the dashboard still runs standalone in demos.
"""

import os
import requests
import pandas as pd

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 3


def api_available() -> bool:
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False


def fetch_regions() -> pd.DataFrame:
    r = requests.get(f"{API_BASE_URL}/regions", timeout=TIMEOUT)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    if not df.empty:
        df["last_updated"] = pd.to_datetime(df["updated_at"])
    return df


def fetch_trends() -> pd.DataFrame:
    r = requests.get(f"{API_BASE_URL}/trends", timeout=TIMEOUT)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def fetch_alerts(limit: int = 20) -> pd.DataFrame:
    r = requests.get(f"{API_BASE_URL}/alerts", params={"limit": limit}, timeout=TIMEOUT)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def fetch_model_scores() -> pd.DataFrame:
    r = requests.get(f"{API_BASE_URL}/models", timeout=TIMEOUT)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def fetch_report() -> str:
    r = requests.get(f"{API_BASE_URL}/report", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()["report"]
