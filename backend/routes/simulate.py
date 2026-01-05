from flask import Blueprint, jsonify
from services.open_meteo_service import fetch_current
from services.cycle_service import process_value
from repositories.telemetry_repo import save_raw
from datetime import datetime

bp = Blueprint("open_meteo", __name__)

@bp.route("/ingest/open-meteo")
def ingest_open_meteo():
    data = fetch_current()
    ts = datetime.utcnow()
    device = "DEV-01"

    mapping = {
        "temp": data["temperature_2m"],
        "pressure": data["pressure_msl"],
        "flow": data["wind_speed_10m"],
    }

    for variable, value in mapping.items():
        save_raw(
            device_id=device,
            ts=ts,
            value=value,
            variable=variable
        )

        process_value(
            device_code=device,
            value=value,
            variable=variable,
            ts=ts
        )

    return jsonify({"status": "ok", "data": mapping})
