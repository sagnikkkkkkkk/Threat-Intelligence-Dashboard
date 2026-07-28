"""
models.py
---------
SQLAlchemy ORM models for the (synthetic) threat-intelligence data layer.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    snapshots = relationship("RegionSnapshot", back_populates="region", cascade="all, delete-orphan")
    activity_points = relationship("ActivityTrendPoint", back_populates="region", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="region", cascade="all, delete-orphan")


class RegionSnapshot(Base):
    """Latest known state for a region (one row kept per region, updated on refresh)."""
    __tablename__ = "region_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    threat_level = Column(String, nullable=False)
    activity_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    region = relationship("Region", back_populates="snapshots")


class ActivityTrendPoint(Base):
    """Historical daily activity score per region, feeds the trend chart."""
    __tablename__ = "activity_trend_points"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    activity_score = Column(Float, nullable=False)

    region = relationship("Region", back_populates="activity_points")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    threat_level = Column(String, nullable=False)
    model_source = Column(String, nullable=False)

    region = relationship("Region", back_populates="alerts")


class ModelScore(Base):
    """Performance metrics for each AI model shown in the dashboard sidebar."""
    __tablename__ = "model_scores"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True, nullable=False)
    task = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=False)
