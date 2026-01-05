from extensions import db

class VariableDefinition(db.Model):
    __tablename__ = "variable_definitions"

    id = db.Column(db.Integer, primary_key=True)

    device_code = db.Column(db.String(50), nullable=False)

    # Nombre visible de la variable (flow, flow_derived, flow_lps)
    name = db.Column(db.String(100), nullable=False)

    # Variable base (None si es RAW)
    source_variable = db.Column(db.String(100), nullable=True)

    # True = RAW, False = DERIVED
    is_raw = db.Column(db.Boolean, default=False)
    
    active = db.Column(db.Boolean, default=True)


    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("device_code", "name", name="uq_device_variable"),
    )

    def __repr__(self):
        return f"<VariableDefinition {self.device_code}:{self.name}>"
