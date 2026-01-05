# Backend - API de Telemetria

## Descripcion general
Este servicio expone una API en Flask que simula telemetria de dispositivos, guarda definiciones y scripts, y calcula variables derivadas ejecutando scripts del usuario. Incluye endpoints para telemetria, administracion de scripts y administracion de variables. Los datos se persisten en PostgreSQL via SQLAlchemy. CORS esta habilitado para el frontend en Vite.

## Tecnologias
- Python 3.12
- Flask 3
- Flask-SQLAlchemy
- PostgreSQL
- Flask-Cors

## Estructura del proyecto
- `app.py`: app factory y registro de blueprints.
- `config.py`: configuracion (DATABASE_URL).
- `extensions.py`: instancias de SQLAlchemy y CORS.
- `routes/`: endpoints (telemetry, scripts, variables).
- `processors/`: pipeline de procesamiento de variables.
- `models/`: modelos de SQLAlchemy (definitions y scripts).
- `services/`: simulador de telemetria, script runner, integraciones externas.
- `repositories/`: helpers de repositorio.
- `admin_scripts/`: utilidades administrativas.

## Requisitos
- Python 3.12+
- PostgreSQL

## Configuracion
Definir la cadena de conexion:

```bash
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/telemetry_db
```

## Ejecucion local
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

La API queda en `http://localhost:5000`.

## Docker
Desde la raiz del repo:

```bash
docker compose up --build
```

Esto levanta Postgres, backend y frontend. El backend usa:
`DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/telemetry_db`.

## API
Base URL: `http://localhost:5000`

### GET /telemetry/<device_code>
Genera un snapshot de telemetria simulado, procesa variables RAW/DERIVED y devuelve los valores.

Ejemplo de respuesta:
```json
{
  "device": "DEV-01",
  "timestamp": "2026-01-05T15:16:00.123456",
  "variables": {
    "temp": 24.5,
    "pressure": 1.12,
    "flow": 6.3,
    "flow_derived_1": 0.0063
  }
}
```

### POST /scripts
Crea o actualiza un script para una variable.

Body:
```json
{
  "device_code": "DEV-01",
  "variable": "flow",
  "code": "var['value'] = var['value'] / 1000"
}
```

Comportamiento:
- Si el objetivo es RAW, crea una DERIVED nueva y guarda el script contra ella.
- Si el objetivo es DERIVED, guarda el script en esa variable.

Ejemplo de respuesta:
```json
{
  "ok": true,
  "target_variable": "flow_derived_1"
}
```

### GET /variables/<device_code>
Lista variables activas del dispositivo.

Ejemplo de respuesta:
```json
[
  {"name": "flow", "is_raw": true, "source": null},
  {"name": "flow_derived_1", "is_raw": false, "source": "flow"}
]
```

### PUT /variables/<device_code>/<variable_name>
Renombra una variable DERIVED (crea una nueva definicion y desactiva la anterior).

Body:
```json
{ "new_name": "flow_m3" }
```

### DELETE /variables/<device_code>/<variable_name>
Elimina una variable DERIVED y sus scripts.

## Modelo de ejecucion de scripts
Los scripts se ejecutan con `exec` usando dos diccionarios:
- `var`: contexto actual (`name`, `value`, `is_raw`, `source`).
- `out`: nuevas variables a emitir (key = name, value = number).

Ejemplo:
```python
# Convertir unidades
var["value"] = var["value"] / 1000
# Renombrar variable
var["name"] = "flow_m3"
# Crear una variable extra
out["flow_avg"] = var["value"]
```

Los scripts se ejecutan en orden por `VariableScript.order`.

## Modelo de datos
- `variable_definitions`: variables del dispositivo (RAW y DERIVED), source, active.
- `variable_scripts`: scripts asociados a variables, ordenados por `order`, active.

## Notas
- La telemetria es simulada en `services/telemetry_simulator.py`.
- La ruta de ingesta Open-Meteo esta en `routes/simulate.py` pero no esta registrada en `app.py`. Ademas importa `services/cycle_service.py`, que no existe. Registrar e implementar si se necesita.