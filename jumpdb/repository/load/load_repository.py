from jumpdb.repository.datasource.datasource_connection import DatasourceConnection
from sqlalchemy import text


class LoadRepository:
    def __init__(self, database, name):
        self.__ds_connection = DatasourceConnection(database=database, name=name)

    def insert(self, stmt, values):
        stmt = text(stmt)

        with self.__ds_connection.get_session() as session:
            result = session.execute(stmt, values)
            session.commit()
            return result.rowcount

    def check_connection(self):
        return self.__ds_connection.check_connection()
