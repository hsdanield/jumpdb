from dataclasses import dataclass

from sqlalchemy import text

from jumpdb.repository.datasource.datasource_connection import DatasourceConnection


@dataclass
class OriginDatabaseRepository:

    def __init__(self, ds_connection: DatasourceConnection):
        self.__ds_connection = ds_connection

    def select(self, stmt):
        data = []
        columns = []
        try:
            with self.__ds_connection.get_session() as session:
                session.begin()
                result = session.execute(text(stmt)).mappings()
                columns = [column for column in result.keys()]
                for row in result:
                    data.append(row)

        except Exception as e:
            print(f"Erro em OriginDatabaseRepository: {e}")

        return columns, data

    def check_connection(self):
        return self.__ds_connection.check_connection()


@dataclass
class DestinyDatabaseRepository:
    def __init__(self, ds_connection: DatasourceConnection):
        self.__ds_connection = ds_connection

    def __create_query_insert(self, table, columns):
        columns_to_string = ", ".join(columns)
        columns_param = ", ".join([str(":") + column for column in columns])
        return f"""INSERT INTO {table} ({columns_to_string}) VALUES({columns_param})"""

    def insert(self, table, columns, values):
        stmt = text(self.__create_query_insert(table=table, columns=columns))

        with self.__ds_connection.get_session() as session:
            result = session.execute(stmt, values)
            session.commit()
            return result.rowcount

    def check_connection(self):
        return self.__ds_connection.check_connection()


@dataclass
class ContractDatabaseRepository:

    def __init__(self, origin_connection: OriginDatabaseRepository, destiny_connection: DestinyDatabaseRepository):
        self.__origin_connection = origin_connection
        self.__destiny_connection = destiny_connection
        self.__check_conn = self.__check_connection()

    def select_origin(self, stmt):
        return self.__origin_connection.select(stmt)

    def insert_destiny(self, table, columns, values):
        return self.__destiny_connection.insert(table, columns, values)

    def __check_connection(self):

        check_conn_origin = self.__origin_connection.check_connection()
        check_conn_destiny = self.__destiny_connection.check_connection()

        if not check_conn_origin and not check_conn_destiny:
            return False
        elif not check_conn_origin:
            print("Falha conexão origem")
            return False
        elif not check_conn_destiny:
            print("Falha conexão destino")
            return False

        return True
