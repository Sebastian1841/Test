from extensions import db


class VariableScript(db.Model):
    __tablename__ = "variable_scripts"

    id = db.Column(db.Integer, primary_key=True)

    device_code = db.Column(db.String(50), nullable=False)

    # Nombre de la variable (debe existir en VariableDefinition)
    variable_name = db.Column(db.String(100), nullable=False)

    order = db.Column(db.Integer, default=1)

    code = db.Column(db.Text, nullable=False)

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.Index("ix_script_device_variable", "device_code", "variable_name"),
    )
