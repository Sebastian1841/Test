from app import create_app
from extensions import db
from models.variable_definition import VariableDefinition

DEVICE_CODE = "DEV-01"
OLD_NAME = "flow_derived"
NEW_NAME = "flow_m3"


def rename_variable():
    app = create_app()

    with app.app_context():
        var = VariableDefinition.query.filter_by(
            device_code=DEVICE_CODE,
            name=OLD_NAME
        ).first()

        if not var:
            print("❌ Variable no encontrada")
            return

        if var.is_raw:
            print("❌ No se puede renombrar una variable RAW")
            return

        exists = VariableDefinition.query.filter_by(
            device_code=DEVICE_CODE,
            name=NEW_NAME
        ).first()

        if exists:
            print("❌ Ya existe una variable con ese nombre")
            return

        var.name = NEW_NAME
        db.session.commit()

        print(f"✅ Variable renombrada: {OLD_NAME} → {NEW_NAME}")


if __name__ == "__main__":
    rename_variable()
