from flask import Flask
from config import Config
from extensions import db, cors
from routes import telemetry_bp, scripts_bp
from routes.variables import variables_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔹 Inicializar extensiones
    db.init_app(app)

    # 🔹 CORS habilitado para el frontend (Vite)
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173"
                ]
            }
        }
    )

    # 🔹 Blueprints
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(scripts_bp)
    app.register_blueprint(variables_bp)

    # 🔹 Crear tablas
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
