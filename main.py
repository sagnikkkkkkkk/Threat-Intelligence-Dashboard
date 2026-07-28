"""
main.py
-------
FastAPI backend for the Threat Intelligence Dashboard prototype.
Serves synthetic data from PostgreSQL (populated via seed.py).

Run:
    uvicorn main:app --reload --port 8000
"""

import os
import sys
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # for data_simulator import

from database import get_db
import models
import schemas
from data_simulator import generate_ai_report
import pandas as pd

app = FastAPI(
    title="Threat Intelligence Dashboard API (Demo)",
    description="Serves SYNTHETIC intelligence data for a prototype dashboard. "
    "Not connected to any real intelligence, satellite, or sensor source.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # relax for local dev; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["meta"])
def root():
    return {
        "service": "threat-dashboard-api",
        "status": "ok",
        "note": "All data served by this API is synthetic / simulated.",
    }


@app.get("/regions", response_model=List[schemas.RegionSnapshotOut], tags=["regions"])
def get_regions(db: Session = Depends(get_db)):
    """Latest snapshot (threat level, activity score, confidence) per region."""
    rows = (
        db.query(models.RegionSnapshot, models.Region)
        .join(models.Region, models.RegionSnapshot.region_id == models.Region.id)
        .all()
    )
    return [
        schemas.RegionSnapshotOut(
            region=region.name,
            lat=region.lat,
            lon=region.lon,
            threat_level=snap.threat_level,
            activity_score=snap.activity_score,
            confidence=snap.confidence,
            updated_at=snap.updated_at,
        )
        for snap, region in rows
    ]


@app.get("/trends", response_model=List[schemas.ActivityTrendOut], tags=["trends"])
def get_trends(region: Optional[str] = None, db: Session = Depends(get_db)):
    """30-day (simulated) activity trend, optionally filtered by region name."""
    query = (
        db.query(models.ActivityTrendPoint, models.Region)
        .join(models.Region, models.ActivityTrendPoint.region_id == models.Region.id)
    )
    if region:
        query = query.filter(models.Region.name == region)
    rows = query.order_by(models.ActivityTrendPoint.date).all()
    if region and not rows:
        raise HTTPException(status_code=404, detail=f"No trend data for region '{region}'")
    return [
        schemas.ActivityTrendOut(region=r.name, date=p.date, activity_score=p.activity_score)
        for p, r in rows
    ]


@app.get("/alerts", response_model=List[schemas.AlertOut], tags=["alerts"])
def get_alerts(limit: int = 20, db: Session = Depends(get_db)):
    """Most recent simulated alerts, newest first."""
    rows = (
        db.query(models.Alert, models.Region)
        .join(models.Region, models.Alert.region_id == models.Region.id)
        .order_by(models.Alert.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        schemas.AlertOut(
            id=a.external_id,
            region=r.name,
            timestamp=a.timestamp,
            message=a.message,
            threat_level=a.threat_level,
            model_source=a.model_source,
        )
        for a, r in rows
    ]


@app.get("/models", response_model=List[schemas.ModelScoreOut], tags=["models"])
def get_model_scores(db: Session = Depends(get_db)):
    """Simulated performance metrics for each AI model used in the pipeline."""
    return db.query(models.ModelScore).all()


@app.get("/report", response_model=schemas.ReportOut, tags=["report"])
def get_report(db: Session = Depends(get_db)):
    """Template-generated intelligence summary based on current region snapshots."""
    rows = (
        db.query(models.RegionSnapshot, models.Region)
        .join(models.Region, models.RegionSnapshot.region_id == models.Region.id)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No region data available")
    df = pd.DataFrame(
        [
            {
                "region": r.name,
                "threat_level": s.threat_level,
                "activity_score": s.activity_score,
                "confidence": s.confidence,
            }
            for s, r in rows
        ]
    )
    return schemas.ReportOut(report=generate_ai_report(df), generated_at=datetime.utcnow())
