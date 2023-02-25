from sqlalchemy import text

from jumpdb.repository.datasource.datasource_connection import DatasourceConnection


class ExtractRepository:

    def __init__(self, database, name):
        self.__ds_connection = DatasourceConnection(database=database, name=name)

    def select(self, stmt):
        data = []
        columns = []
        try:
            with self.__ds_connection.get_session() as session:
                stmt = text(stmt)
                session.begin()
                result = session.execute(stmt).mappings()
                columns = [column for column in result.keys()]
                for row in result:
                    data.append(row)

        except Exception as e:
            print(f"Erro em OriginDatabaseRepository: {e}")

        return columns, data

    def check_connection(self):
        return self.__ds_connection.check_connection()
