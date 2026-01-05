from models.variable_definition import VariableDefinition
from models.variable_script import VariableScript
from services.script_runner import run_script
from extensions import db


class VariableProcessor:

    def process_snapshot(self, device_code, raw_vars, timestamp):
        result = {}

        # =====================================================
        # 1️⃣ Registrar variables RAW
        # =====================================================
        for name, value in raw_vars.items():
            result[name] = value

            raw_def = VariableDefinition.query.filter_by(
                device_code=device_code,
                name=name
            ).first()

            if not raw_def:
                db.session.add(VariableDefinition(
                    device_code=device_code,
                    name=name,
                    is_raw=True,
                    active=True
                ))

        db.session.commit()

        # =====================================================
        # 2️⃣ Procesar SOLO DERIVED ACTIVAS
        # =====================================================
        derived_defs = VariableDefinition.query.filter_by(
            device_code=device_code,
            is_raw=False,
            active=True
        ).all()

        for d in derived_defs:
            base_value = result.get(d.source_variable)
            if base_value is None:
                continue

            var = {
                "name": d.name,
                "value": base_value,
                "is_raw": False,
                "source": d.source_variable,
            }
            out = {}

            scripts = VariableScript.query.filter_by(
                device_code=device_code,
                variable_name=d.name,
                active=True
            ).order_by(VariableScript.order).all()

            for s in scripts:
                var, out = run_script(s.code, var, out)

            final_name = var.get("name", d.name)
            final_value = var.get("value")

            # =================================================
            # 🔁 RENAME ONE-SHOT
            # =================================================
            if final_name != d.name:
                # crear nueva definición si no existe
                new_def = VariableDefinition.query.filter_by(
                    device_code=device_code,
                    name=final_name
                ).first()

                if not new_def:
                    new_def = VariableDefinition(
                        device_code=device_code,
                        name=final_name,
                        source_variable=d.source_variable,
                        is_raw=False,
                        active=True
                    )
                    db.session.add(new_def)
                    db.session.commit()

                # 🔴 desactivar la variable antigua
                d.active = False
                db.session.commit()

                # copiar scripts SOLO si la nueva no tiene
                has_scripts = VariableScript.query.filter_by(
                    device_code=device_code,
                    variable_name=final_name
                ).count()

                if has_scripts == 0:
                    for old_s in scripts:
                        db.session.add(VariableScript(
                            device_code=device_code,
                            variable_name=final_name,
                            order=old_s.order,
                            code=old_s.code,
                            active=old_s.active
                        ))
                    db.session.commit()

            # =================================================
            # Guardar resultado principal
            # =================================================
            if final_value is not None:
                result[final_name] = final_value

            # =================================================
            # Guardar variables nuevas generadas por `out`
            # =================================================
            for new_name, new_value in out.items():
                if new_value is None:
                    continue

                exists = VariableDefinition.query.filter_by(
                    device_code=device_code,
                    name=new_name
                ).first()

                if not exists:
                    db.session.add(VariableDefinition(
                        device_code=device_code,
                        name=new_name,
                        source_variable=d.source_variable,
                        is_raw=False,
                        active=True
                    ))
                    db.session.commit()

                result[new_name] = new_value

        return result
