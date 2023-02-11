from dataclasses import dataclass

import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword


@dataclass
class ColumnsMandatory:
    ID = "ID VARCHAR2(32) NOT NULL"
    DTC_INICIO = "DTC_INICIO DATE"
    DTC_FIM = "DTC_FIM DATE"
    STS_CORRENTE = "STS_CORRENTE VARCHAR2(1)"


def get_tables(sql):
    stmt = sqlparse.parse(sql)[0]
    tables = []
    for item in stmt.tokens:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                if identifier.ttype is Keyword:
                    tables.append(str(identifier))
        elif isinstance(item, Identifier):
            if item.ttype is Keyword:
                tables.append(str(item))
    return tables


def get_columns(sql):
    stmt = sqlparse.parse(sql)[0]
    columns = []

    for item in stmt.tokens:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                if identifier.ttype is not Keyword:
                    columns.append(str(identifier))

        elif isinstance(item, Identifier):
            if item.ttype is not Keyword:
                columns.append(str(item))

    return columns


def get_tables_and_columns(sql):
    stmt = sqlparse.parse(sql)[0]
    data = []
    tables = []
    columns = []

    for token in stmt.tokens:
        if isinstance(token, Identifier):
            tables.append(
                {
                    "alias_table": str(token.get_alias()).lower(),
                    "real_name": str(token.get_real_name()).lower(),
                    "full_name": str(token).lower()
                }
            )

        elif isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                if identifier.ttype is not Keyword and identifier.has_alias():
                    columns.append(
                        {
                            "alias_column": str(identifier.get_alias()).lower(),
                            "real_name": str(identifier.get_real_name()).lower(),
                            "alias_table": str(get_alias_dot(str(identifier))).lower(),
                            "full_name": str(identifier).lower()
                        }
                    )

    for table in tables:
        data.append(
            [
                {"table": table},
                {"columns": [column for column in columns if column["alias_table"] == table["alias_table"]]}
            ]
        )

    for obj in data:
        obj[1]["columns"] = sorted(obj[1]["columns"], key=lambda x: x["real_name"])

    return {"data": data}


def get_alias_dot(content: str):
    if content.count(".") > 0:
        return str(content)[0:str(content).find(".")]

    return None


def create_pk(table):
    return "ALTER TABLE {} ADD CONSTRAINT PK_{} PRIMARY KEY (ID);".format(table, table)


def create_columns(columns):
    data = []
    for column in columns:
        data.append(
            "\n\t{} {}, --{}.{}".format(str(column["alias_column"]),
                                        str(column["precision"]),
                                        str(column["table_name"]),
                                        str(column["real_name"]))
        )
    return "".join(data)


def query_create_table(table, columns):
    return """CREATE TABLE {} (\n\t{},{},\n\t{},\n\t{},\n\t{}\n);\n\n{}""".format(table,
                                                                                  ColumnsMandatory.ID,
                                                                                  create_columns(columns),
                                                                                  ColumnsMandatory.DTC_INICIO,
                                                                                  ColumnsMandatory.DTC_FIM,
                                                                                  ColumnsMandatory.STS_CORRENTE,
                                                                                  create_pk(table)).upper()
