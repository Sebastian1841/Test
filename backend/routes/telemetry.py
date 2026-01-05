from flask import Blueprint, jsonify
from services.telemetry_simulator import generate_last_telemetry
from processors.variable_processor import VariableProcessor

telemetry_bp = Blueprint("telemetry", __name__)

processor = VariableProcessor()


@telemetry_bp.route("/telemetry/<device_code>")
def telemetry(device_code):
    # 🔹 1. Obtener última telemetría cruda
    telemetry = generate_last_telemetry(device_code)

    # 🔹 2. Procesar RAW + DERIVED según definiciones
    variables = processor.process_snapshot(
        device_code=device_code,
        raw_vars=telemetry["variables"],
        timestamp=telemetry["timestamp"]
    )

    # 🔹 3. Responder al frontend
    return jsonify({
        "device": device_code,
        "timestamp": telemetry["timestamp"].isoformat(),
        "variables": variables
    })
