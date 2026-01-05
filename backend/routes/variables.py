from flask import Blueprint, jsonify, request
from models.variable_definition import VariableDefinition
from models.variable_script import VariableScript 
from extensions import db


variables_bp = Blueprint("variables", __name__)


# =====================================================
# 🔹 LISTAR VARIABLES (SOLO ACTIVAS)
# =====================================================
@variables_bp.route("/variables/<device_code>", methods=["GET"])
def list_variables(device_code):
    vars = VariableDefinition.query.filter_by(
        device_code=device_code,
        active=True
    ).all()

    return jsonify([
        {
            "name": v.name,
            "is_raw": v.is_raw,
            "source": v.source_variable
        }
        for v in vars
    ])


# =====================================================
# ✏️ RENOMBRAR VARIABLE DERIVED (CREA NUEVA + DESACTIVA VIEJA)
# =====================================================
@variables_bp.route("/variables/<device_code>/<variable_name>", methods=["PUT"])
def rename_variable(device_code, variable_name):
    data = request.get_json() or {}
    new_name = data.get("new_name")

    if not new_name:
        return jsonify({"error": "new_name is required"}), 400

    # Variable actual
    old_var = VariableDefinition.query.filter_by(
        device_code=device_code,
        name=variable_name,
        active=True
    ).first()

    if not old_var:
        return jsonify({"error": "Variable not found"}), 404

    # 🔒 RAW no se puede renombrar
    if old_var.is_raw:
        return jsonify({"error": "RAW variables cannot be renamed"}), 400

    # 🔒 Evitar duplicados
    exists = VariableDefinition.query.filter_by(
        device_code=device_code,
        name=new_name,
        active=True
    ).first()

    if exists:
        return jsonify({"error": "Variable name already exists"}), 400

    # ✅ Crear NUEVA variable DERIVED
    new_var = VariableDefinition(
        device_code=device_code,
        name=new_name,
        source_variable=old_var.source_variable,
        is_raw=False,
        active=True
    )
    db.session.add(new_var)

    # 🔴 Desactivar la antigua
    old_var.active = False

    db.session.commit()

    return jsonify({
        "ok": True,
        "old_name": variable_name,
        "new_name": new_name
    })

@variables_bp.route("/variables/<device_code>/<variable_name>", methods=["DELETE"])
def delete_variable(device_code, variable_name):

    var = VariableDefinition.query.filter_by(
        device_code=device_code,
        name=variable_name
    ).first()

    if not var:
        return jsonify({"error": "Variable not found"}), 404

    # 🔒 No permitir borrar RAW
    if var.is_raw:
        return jsonify({"error": "RAW variables cannot be deleted"}), 400

    # 🧹 Borrar scripts asociados
    VariableScript.query.filter_by(
        device_code=device_code,
        variable_name=variable_name
    ).delete()

    # 🧹 Borrar definición
    db.session.delete(var)
    db.session.commit()

    return jsonify({
        "ok": True,
        "deleted": variable_name
    })
