from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from jumpdb.utils.file_util import write_csv, write_json
from jumpdb.cli.validator.cli_validator import validate_format
from jumpdb.serializers.etl_database_serial import OriginMapping
from jumpdb.service.etl.etl_database import extract_select

etl_database = typer.Typer(help="ETL Database", name="etl_database")
console = Console()


@etl_database.command("extract_select")
def select(
        database: str,
        name: str,
        stmt: str,
        path_file: str = typer.Option(...),
        out_format: str = typer.Option(..., help="Formato de saida do arquivo (csv, json)"),
        show: bool = Optional[False]
):
    """
    Select no banco de dados
    :param database: tipo do banco de dados (oracle, mysql, postgresql)
    :param name: nome chave em settings.toml
    :param stmt: select desejado
    :param path_file: caminho para salvar o arquivo
    :param out_format: formato de saida do arquivo
    :param show: Mostrar no console o resultado
    """

    validate_format(out_format)

    map_in = OriginMapping(database=database, name=name, select=stmt)
    map_out = extract_select(map_in)

    if out_format == "csv":
        write = write_csv(path_file=path_file, dict_data=map_out.data, columns=map_out.columns)
        if write:
            console.print(f"Arquivo gravador com sucesso do tipo {out_format}... path: {path_file}")
        else:
            console.print(f"Ocorreu algum erro ao salvar arquivo do tipo {out_format}")

    elif out_format == "json":
        write = write_json(path_file=path_file, dict_data=map_out.data)
        if write:
            console.print(f"Arquivo gravado com sucesso do tipo {out_format}... path: {path_file}")
        else:
            console.print(f"Erro ao salvar arquivo do tipo {out_format}")

    if show:
        table = Table(title=f"Extract Select")
        [table.add_column(header, style="magenta") for header in map_out.columns]
        for item in map_out.data:
            row = [str(item[header]) for header in map_out.columns]
            table.add_row(*row)

        console.print(table)
