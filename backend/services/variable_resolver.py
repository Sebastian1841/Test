from models.variable_definition import VariableDefinition

def get_variable_definition(device_code, name):
    return VariableDefinition.query.filter_by(
        device_code=device_code,
        name=name
    ).first()
