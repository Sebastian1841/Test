from extensions import db
from datetime import datetime

class TelemetrySnapshot(db.Model):
    __tablename__ = "telemetry_snapshots"

    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String, nullable=False)
    variable = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
