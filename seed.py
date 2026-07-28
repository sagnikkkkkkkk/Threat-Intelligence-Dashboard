"""
seed.py
-------
Creates tables (if needed) and populates PostgreSQL with synthetic data
using the same generator logic as the original prototype
(../data_simulator.py). Run this once after setting up the database:

    python seed.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # for data_simulator import

from database import Base, engine, SessionLocal
from models import Region, RegionSnapshot, ActivityTrendPoint, Alert, ModelScore
from data_simulator import (
    generate_region_snapshot,
    generate_activity_trend,
    generate_alerts,
    generate_model_scores,
)


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Wipe existing data for a clean reseed
        db.query(Alert).delete()
        db.query(ActivityTrendPoint).delete()
        db.query(RegionSnapshot).delete()
        db.query(ModelScore).delete()
        db.query(Region).delete()
        db.commit()

        region_snapshot_df = generate_region_snapshot()
        trend_df = generate_activity_trend()
        alerts_df = generate_alerts()
        models_df = generate_model_scores()

        region_objs = {}
        for _, row in region_snapshot_df.iterrows():
            region = Region(name=row["region"], lat=row["lat"], lon=row["lon"])
            db.add(region)
            db.flush()  # get region.id
            region_objs[row["region"]] = region

            db.add(
                RegionSnapshot(
                    region_id=region.id,
                    threat_level=row["threat_level"],
                    activity_score=row["activity_score"],
                    confidence=row["confidence"],
                    updated_at=row["last_updated"],
                )
            )

        for _, row in trend_df.iterrows():
            region = region_objs.get(row["region"])
            if region:
                db.add(
                    ActivityTrendPoint(
                        region_id=region.id,
                        date=row["date"],
                        activity_score=row["activity_score"],
                    )
                )

        for _, row in alerts_df.iterrows():
            region = region_objs.get(row["region"])
            if region:
                db.add(
                    Alert(
                        external_id=row["id"],
                        region_id=region.id,
                        timestamp=row["timestamp"],
                        message=row["message"],
                        threat_level=row["threat_level"],
                        model_source=row["model_source"],
                    )
                )

        for _, row in models_df.iterrows():
            db.add(
                ModelScore(
                    model=row["model"],
                    task=row["task"],
                    accuracy=row["accuracy"],
                    latency_ms=row["latency_ms"],
                )
            )

        db.commit()
        print(f"Seeded {len(region_objs)} regions, {len(trend_df)} trend points, "
              f"{len(alerts_df)} alerts, {len(models_df)} model scores.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
