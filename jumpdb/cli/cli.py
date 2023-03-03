from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table

from jumpdb.cli.validator.cli_validator import validate_format
from jumpdb.serializers.etl_database_serial import OriginMapping
from jumpdb.serializers.inspector_serial import ColumnsIn, InspectorIn
from jumpdb.service.etl.etl_database import extract_select
from jumpdb.service.inserpector.inspector_service import (get_columns,
                                                          get_pk_constraint,
                                                          get_foreign_keys,
                                                          get_indexes,
                                                          mapping_column_type)
from jumpdb.utils.file_util import read_file, write_json, write_csv
from jumpdb.utils.sql_parser_util import query_create_table
from jumpdb.utils.table_util import (header_columns, header_constraints, header_fks, header_indexes)

main = typer.Typer(help="JumperDB Application")
console = Console()


@main.command("columns")
def columns(
        database: str,
        name: str,
        table_name: str = typer.Option(...),
        filter_columns: Optional[List[str]] = None
):
    """Buscar Colunas e inspecionar seus tipos e comentarios no banco de dados
       database: informar dialect (por exemplo mysql ou oracle)
       name: informar o nome cadastros em settings.toml
       table_name: nome da tabela para busca
       filter_columns: caso não informado ira recuperar todas as colunas
    """

    map_in = ColumnsIn(database=database,
                       name=name,
                       table_name=table_name,
                       filter_columns=filter_columns)

    inspector_out = get_columns(map_in)

    headers = header_columns()

    table = Table(title=f"Summary Table {table_name}")

    [table.add_column(header, style="magenta") for header in headers]

    # # Add data rows
    for item in inspector_out:
        row = [str(getattr(item, header)) for header in headers]
        table.add_row(*row)

    console.print(table)


@main.command("pks")
def pks(
        database: str,
        name: str,
        table_name: str = typer.Option(...)
):
    """Buscar Primary Keys no banco de dados
       database: informar dialect (por exemplo mysql ou oracle)
       name: informar o nome cadastros em settings.toml
       table_name: nome da tabela para busca
    """

    map_in = InspectorIn(database=database, name=name, table_name=table_name)

    map_out = get_pk_constraint(map_in)

    headers = header_constraints()

    table = Table(title=f"PKS {table_name}")
    [table.add_column(header, style="magenta") for header in headers]

    row = [str(getattr(map_out, header)) for header in headers]
    table.add_row(*row)

    console.print(table)


@main.command("fks")
def fks(
        database: str,
        name: str,
        table_name: str = typer.Option(...)
):
    """Buscar Foreign Keys no banco de dados
       database: informar dialect (por exemplo mysql ou oracle)
       name: informar o nome cadastros em settings.toml
       table_name: nome da tabela para busca
    """

    map_in = InspectorIn(database=database, name=name, table_name=table_name)

    map_out = get_foreign_keys(map_in)

    headers_constraint = header_constraints()
    headers_fks = header_fks()

    table = Table(title=f"FKS {table_name}")
    [table.add_column(header, style="magenta") for header in [*headers_constraint, *headers_fks]]

    for item in map_out:
        row_constraint = [str(getattr(getattr(item, "constraint_out"), header)) for header in headers_constraint]
        row_fks = [str(getattr(item, header)) for header in headers_fks]

        row = [*row_constraint, *row_fks]
        table.add_row(*row)

    console.print(table)


@main.command("indexes")
def indexes(
        database: str,
        name: str,
        table_name: str = typer.Option(...)
):
    """Buscar Indexes de uma tabela no banco de dados
       database: informar dialect (por exemplo mysql ou oracle)
       name: informar o nome cadastros em settings.toml
       table_name: nome da tabela para busca
    """

    map_in = InspectorIn(database=database,
                         name=name,
                         table_name=table_name)

    map_out = get_indexes(map_in)

    headers_constraint = header_constraints()
    headers_indexes = header_indexes()

    table = Table(title=f"Indexes {table_name}")
    [table.add_column(header, style="magenta") for header in [*headers_constraint, *headers_indexes]]

    for item in map_out:
        row_constraint = [str(getattr(getattr(item, "constraint_out"), header)) for header in headers_constraint]
        row_fks = [str(getattr(item, header)) for header in headers_indexes]

        row = [*row_constraint, *row_fks]
        table.add_row(*row)

    console.print(table)


@main.command("summary_table")
def summary_table(
        database: str,
        name: str,
        table_name: str = typer.Option(...)
):
    """
    Buscar Colunas, Primary Keys, Foreign Key, Indexes
    :param database: tipo do banco de dados (oracle, mysql, postgresql)
    :param name: nome chave em settings.toml
    :param table_name: nome da tabela do banco de dados
    """
    map_in = InspectorIn(database=database,
                         name=name,
                         table_name=table_name)

    columns(map_in.database, map_in.name, map_in.table_name)
    pks(map_in.database, map_in.name, map_in.table_name)
    fks(map_in.database, map_in.name, map_in.table_name)
    indexes(map_in.database, map_in.name, map_in.table_name)


@main.command("extract_select")
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


@main.command("mapping")
def mapping(
        database: str,
        name: str,
        # database_origem: str = typer.Option(...),
        new_table: str = typer.Option(...),
        path_file: str = typer.Option(...)
):
    """Gerar script de acordo com uma select Mapeada
       database: informar dialect (por exemplo mysql ou oracle)
       name: informar o nome cadastros em settings.toml
       new_table: nome da tabela de geração
       path_file: caminho do arquivo do SELECT
    """
    content = read_file(path_file)

    mapping_column = mapping_column_type(database=database,
                                         name=name,
                                         content=content)

    query = query_create_table(new_table, columns=mapping_column)

    console.print(query)

#
# @main.command("etl")
# def origin_destiny(
#         name_origin: str,
#         name_destiny: str,
#         type_origin: str = typer.Option(...),
#         type_destiny: str = typer.Option(...),
#         select: str = typer.Option(...),
#         table_destiny=typer.Option(...),
#
# ):
#     name_origin.title()
#
#     table = Table(title="ETL DATABASE")
#     table.add_column("Origin", style="magenta")
#     table.add_column("Destiny", style="magenta")
#
#     table.add_row(name_origin, name_destiny)
#     table.add_row(type_origin, type_destiny)
#
#     stmt_oracle = """data_dest"""
#
#     conn_origin = DatasourceConnection(database=type_origin, name=name_origin)
#     conn_destiny = DatasourceConnection(database=type_destiny, name=name_destiny)
#     origin = OriginDatabaseRepository(ds_connection=conn_origin)
#     destiny = DestinyDatabaseRepository(ds_connection=conn_destiny)
#     contract = ContractDatabaseRepository(origin_connection=origin, destiny_connection=destiny)
#     columns, values = contract.select_origin(select)
#     row_count = contract.insert_destiny(table=table_destiny, columns=columns, values=values)
#
#     console.print(table)
#     console.print(f"Total de linhas inseridas: {row_count}")
