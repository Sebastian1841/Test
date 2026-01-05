def run_script(code: str, var: dict, out: dict):
    if not code or not code.strip():
        return var, out

    # 🔑 UNA sola fuente de verdad
    ctx = {
        "var": var,
        "out": out,
    }

    exec(code, {}, ctx)

    return ctx["var"], ctx["out"]
