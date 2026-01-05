import random
from datetime import datetime

def generate_last_telemetry(device_id):
    return {
        "device_id": device_id,
        "timestamp": datetime.utcnow(),
        "variables": {
            "temp": round(random.uniform(18, 30), 1),
            "flow": random.choice([0, 0, 0, round(random.uniform(1, 15), 1)]),
            "pressure": round(random.uniform(0.8, 1.6), 2)
        }
    }