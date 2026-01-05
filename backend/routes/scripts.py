from flask import Blueprint, request, jsonify
from models.variable_definition import VariableDefinition
from models.variable_script import VariableScript
from extensions import db

scripts_bp = Blueprint("scripts", __name__)


@scripts_bp.route("/scripts", methods=["POST"])
def save_script():
    data = request.json or {}

    device = data.get("device_code")
    variable = data.get("variable")
    code = data.get("code")

    if not device or not variable or not code:
        return jsonify({"error": "device_code, variable and code are required"}), 400

    # =====================================================
    # 1️⃣ Buscar definición
    # =====================================================
    definition = VariableDefinition.query.filter_by(
        device_code=device,
        name=variable,
        active=True
    ).first()

    if not definition:
        return jsonify({"error": "Variable not found"}), 404

    # =====================================================
    # 2️⃣ DECISIÓN CLAVE: RAW vs DERIVED
    # =====================================================

    # 🔹 CASO A: RAW → crear DERIVED NUEVA
    if definition.is_raw:
        base = definition.name

        # contar cuántas DERIVED ya existen desde esta RAW
        count = VariableDefinition.query.filter_by(
            device_code=device,
            source_variable=base
        ).count()

        derived_name = f"{base}_derived_{count + 1}"

        derived = VariableDefinition(
            device_code=device,
            name=derived_name,
            source_variable=base,
            is_raw=False,
            active=True
        )
        db.session.add(derived)
        db.session.commit()

        target_variable = derived_name

    # 🔹 CASO B: DERIVED → modificar la misma
    else:
        target_variable = definition.name

    # =====================================================
    # 3️⃣ Guardar script en la variable correcta
    # =====================================================
    script = VariableScript(
        device_code=device,
        variable_name=target_variable,
        code=code,
        active=True
    )

    db.session.add(script)
    db.session.commit()

    return jsonify({
        "ok": True,
        "target_variable": target_variable
    })
