class TelemetryRepository:
    def __init__(self):
        self._state = {}  # device -> variable -> snapshot

    def get_last(self, device_id: str, variable: str):
        return self._state.get(device_id, {}).get(variable)

    def save(self, snapshot):
        self._state.setdefault(snapshot.device_id, {})
        self._state[snapshot.device_id][snapshot.variable] = snapshot