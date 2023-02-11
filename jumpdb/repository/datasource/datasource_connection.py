from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from jumpdb.configs.config import settings


class DatasourceConnection:

    def __init__(self, database, name):
        self.__drivername = settings.datasources[database][name]["drivername"]
        self.__username = settings.datasources[database][name]["username"]
        self.__password = settings.datasources[database][name]["password"]
        self.__host = settings.datasources[database][name]["host"]
        self.__database = settings.datasources[database][name]["database"]
        self.__port = settings.datasources[database][name]["port"]
        self.__query = settings.datasources[database][name]["query"]
        self.__engine = self.__create_engine()

    def __create_engine(self):
        try:
            return create_engine(self.__get_url())

        except Exception as e:
            print(f"Erro ao criar engine {e}")

    def __get_url(self):
        return URL.create(
            drivername=self.__drivername,
            username=self.__username,
            password=self.__password,
            host=self.__host,
            database=self.__database,
            port=self.__port,
            query=self.__query
        )

    def get_session(self):
        return Session(self.__engine)

    def get_engine(self):
        return self.__engine
