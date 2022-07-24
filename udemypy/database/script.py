import os


def get_path(script_name: str) -> str:
    database_dir = os.path.dirname(__file__)
    scripts_dir = os.path.join(database_dir, "scripts")
    return os.path.join(scripts_dir, script_name)


def set_variables_value(sql_script: str, variables: dict):
    if not variables:
        return sql_script

    for variable, value in variables.items():
        if isinstance(value, str):
            sql_script = sql_script.replace(variable, f"'{value}'")
        else:
            sql_script = sql_script.replace(variable, str(value))

    return sql_script
