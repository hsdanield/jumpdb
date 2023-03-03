from typer import Typer

from jumpdb.cli.inspector_cli import inspector
from jumpdb.cli.etl_database_cli import etl_database

main = Typer(help="JumperDB Application")
main.add_typer(inspector)
main.add_typer(etl_database)
