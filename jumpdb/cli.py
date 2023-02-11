from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import Table

from jumpdb.service.connection_service import (get_columns,
                                               get_pk_constraint,
                                               get_foreign_keys,
                                               get_indexes,
                                               mapping_column_type)

from jumpdb.utils.sql_parser_util import query_create_table
from jumpdb.utils.table_util import header_columns, header_pks, header_fks, header_indexes
from jumpdb.utils.file_util import read_file

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
    data = get_columns(database=database,
                       name=name,
                       table_name=table_name,
                       filter_columns=filter_columns)

    headers = header_columns()

    table = Table(title=f"Summary Table {table_name}")

    [table.add_column(header, style="magenta") for header in headers]

    # Add data rows
    for item in data:
        row = [str(item[header]) for header in headers]
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
    data = get_pk_constraint(database=database,
                             name=name,
                             table_name=table_name)

    headers = header_pks()

    table = Table(title=f"PKS {table_name}")
    [table.add_column(header, style="magenta") for header in headers]
    table.add_row(str(data["name"]), str(data["constrained_columns"]))

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
    data = get_foreign_keys(database=database,
                            name=name,
                            table_name=table_name)

    headers = header_fks()

    table = Table(title=f"PKS {table_name}")
    [table.add_column(header, style="magenta") for header in headers]

    for item in data:
        row = [str(item[header]) for header in headers]
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

    data = get_indexes(database=database,
                       name=name,
                       table_name=table_name)

    headers = header_indexes()

    table = Table(title=f"PKS {table_name}")
    [table.add_column(header, style="magenta") for header in headers]

    for item in data:
        row = [str(item[header]) for header in headers]
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
