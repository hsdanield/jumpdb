from sqlalchemy import inspect

from .datasource.datasource_connection import DatasourceConnection


class DatasourceInspect:

    def __init__(self, ds_connection: DatasourceConnection):
        self.__ds_connection = ds_connection
        self.__inspector = inspect(self.__ds_connection.get_engine())

    def get_table_names(self, table_name):
        return self.__inspector.get_table_names(table_name)

    def get_columns(self, table_name, filter_columns):

        if not filter_columns:
            columns = self.__inspector.get_columns(table_name)
        else:
            columns = [c for c in self.__inspector.get_columns(table_name)
                       if c["name"] in filter_columns]

        for column in columns:
            column["precision"] = str(column["type"].as_generic())

        for column in columns:
            for key, value in column.items():
                column[key] = str(value)

        return columns

    def get_pk_constraint(self, table_name):
        return self.__inspector.get_pk_constraint(table_name)

    def get_foreign_keys(self, table_name):
        return self.__inspector.get_foreign_keys(table_name)

    def get_indexes(self, table_name):
        return self.__inspector.get_indexes(table_name)

    def summary_pk_fk(self, table_name, filter_columns=None):

        columns = filter_columns

        if columns is None:
            columns = self.__inspector.get_columns(table_name)
        else:
            columns = [c for c in self.__inspector.get_columns(table_name) if c["name"] in columns]

        return {

            "columns": columns,
            "PKs or Unique": self.__inspector.get_pk_constraint(table_name),
            "FKs": self.__inspector.get_foreign_keys(table_name),
            "comment": self.__inspector.get_table_comment(table_name)

        }

    def get_engine(self):
        return self.__ds_connection.get_engine()
