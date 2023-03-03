import typer


def validate_format(value: str):
    if value not in ["csv", "json"]:
        raise typer.BadParameter("--out-format deve ser 'csv' ou 'json'.")
    return value
