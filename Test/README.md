# Frontend - Consola de Telemetria

## Descripcion general
Frontend en Vue 3 + Vite para visualizar telemetria y editar scripts de variables. Se conecta a la API en Flask y ofrece un editor Monaco con plantillas para transformaciones comunes.

## Funcionalidades
- Obtener y mostrar la ultima telemetria
- Selector de variables con etiqueta RAW/DERIVED
- Editor de scripts con plantillas y autocompletado
- Eliminacion de variables derivadas

## Tecnologias
- Vue 3
- Vite
- Tailwind CSS
- Monaco Editor

## Requisitos
- Node.js 20+
- Backend activo en `http://localhost:5000`

## Ejecucion local
```bash
npm install
npm run dev
```

Abrir `http://localhost:5173`.

## Build
```bash
npm run build
npm run preview
```

## Configuracion
La URL base de la API esta hardcodeada en:
- `src/services/telemetry.service.js`
- `src/services/variable.service.js`
- `src/services/script.service.js`

Actualizar `API_URL` si el backend corre en otra direccion.

## Docker
Se puede levantar el stack completo desde la raiz:

```bash
docker compose up --build
```

O construir la imagen del frontend desde `Test/Dockerfile`.

## Estructura del proyecto
- `src/views/`: vistas de telemetria y scripts.
- `src/components/`: UI de tabla de telemetria y editor de scripts.
- `src/services/`: clientes HTTP.
- `src/stores/`: helpers de estado para variables y telemetria.