class ScriptRepository:
    def __init__(self):
        self._scripts = []  # lista de VariableScript

    def get_scripts(self, device_id: str, variable: str):
        return sorted(
            [
                s for s in self._scripts
                if s.device_id == device_id
                and s.variable == variable
                and s.active
            ],
            key=lambda s: s.order
        )

    def add_script(self, script):
        self._scripts.append(script)