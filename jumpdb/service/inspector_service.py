from jumpdb.repository.datasource.datasource_connection import DatasourceConnection
from jumpdb.repository.inspect_repository import DatasourceInspect


def create_inspector(database, name):
    inspector = None
    try:
        connection = DatasourceConnection(database, name)
        inspector = DatasourceInspect(connection)
    except Exception as e:
        print(f"Ops! Erro em create_inspector: {e}")

    return inspector
