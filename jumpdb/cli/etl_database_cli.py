from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from jumpdb.utils.file_util import write_csv, write_json
from jumpdb.cli.validator.cli_validator import validate_format
from jumpdb.serializers.etl_database_serial import OriginMap, FileMap, ExtSltMapSaveFileIn
from jumpdb.service.etl.etl_database import ext_slt, ext_slt_save_file

etl_database = typer.Typer(help="ETL Database", name="etl_database")
console = Console()


@etl_database.command("ext_select")
def ext_select(
        database: str,
        name: str,
        stmt: str,
):
    """
    Select no banco de dados
    :param database: tipo do banco de dados (oracle, mysql, postgresql)
    :param name: nome chave em settings.toml
    :param stmt: select desejado
    """
    map_in = OriginMap(database=database, name=name, select=stmt)
    map_out = ext_slt(map_in)

    table = Table(title=f"Extract Select")
    [table.add_column(header, style="magenta") for header in map_out.columns]
    for item in map_out.data:
        row = [str(item[header]) for header in map_out.columns]
        table.add_row(*row)

    console.print(table)


@etl_database.command("ext_slt_save_file")
def slt_save_file(
        database: str,
        name: str,
        stmt: str,
        path_file: str = typer.Option(...),
        format_file: str = typer.Option(..., help="Formato de saida do arquivo (csv, json)"),
):
    """
    Gravar arquivo de acordo com Select no banco de dados
    :param database: tipo do banco de dados (oracle, mysql, postgresql)
    :param name: nome chave em settings.toml
    :param stmt: select desejado
    :param path_file: caminho para salvar o arquivo
    :param format_file: formato de saida do arquivo
    """

    validate_format(format_file)

    origin_map = OriginMap(database=database, name=name, select=stmt)
    file_map = FileMap(path_file=path_file, format_file=format_file)
    map_in = ExtSltMapSaveFileIn(origin=origin_map, file=file_map)
    map_out = ext_slt_save_file(map_in)

    # Se foi gravado com sucesso
    if map_out.is_write:
        console.print(f"Arquivo gravado com sucesso do tipo {format_file}... path: {path_file}")
    else:
        console.print(f"Erro ao gravar arquivo do tipo {format_file}... path: {path_file}")
