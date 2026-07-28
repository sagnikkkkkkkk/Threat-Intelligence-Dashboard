"""
schemas.py
----------
Pydantic response/request models for the FastAPI layer.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RegionSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    region: str
    lat: float
    lon: float
    threat_level: str
    activity_score: float
    confidence: float
    updated_at: datetime


class ActivityTrendOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    region: str
    date: datetime
    activity_score: float


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    region: str
    timestamp: datetime
    message: str
    threat_level: str
    model_source: str


class ModelScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: str
    task: str
    accuracy: float
    latency_ms: float


class ReportOut(BaseModel):
    report: str
    generated_at: datetime
