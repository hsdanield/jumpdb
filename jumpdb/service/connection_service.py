from jumpdb.utils.sql_parser_util import get_tables_and_columns
from .inspector_service import create_inspector


def get_columns(database, name, table_name, filter_columns):
    data = None

    try:

        inspector = create_inspector(database=database, name=name)
        data = inspector.get_columns(table_name, filter_columns)

    except Exception as e:
        print(f"Ops! Erro em get_columns: {e}")

    return data


def get_pk_constraint(database, name, table_name):
    data = None
    try:
        inspector = create_inspector(database, name)
        data = inspector.get_pk_constraint(table_name=table_name)

    except Exception as e:
        print(f"Ops! Erro em get_pk_constraint: {e}")

    return data


def get_foreign_keys(database, name, table_name):
    data = None
    try:
        inspector = create_inspector(database, name)
        data = inspector.get_foreign_keys(table_name=table_name)

    except Exception as e:
        print(f"Ops! Erro em get_foreign_keys: {e}")

    return data


def get_indexes(database, name, table_name):
    data = None
    try:
        inspector = create_inspector(database, name)
        data = inspector.get_indexes(table_name=table_name)

    except Exception as e:
        print(f"Ops! Erro em get_indexes: {e}")

    return data


def mapping_column_type(database, name, content):
    mapping = []
    columns_map = []

    i = 0
    data = get_tables_and_columns(content)["data"]
    for item in data:
        table = item[0]["table"]
        columns = item[1]["columns"]

        if columns:

            columns_map = [(column["real_name"], column["alias_column"]) for column in columns if column]

            searchcolumns = get_columns(database=database,
                                        name=name,
                                        table_name=table["real_name"],
                                        filter_columns=sorted([column[0] for column in columns_map if columns]))
            for sc in searchcolumns:
                mapping.append(
                    *[
                        {
                            "real_name": real_name,
                            "alias_column": alias_column,
                            "precision": sc["precision"],
                            "table_name": table["real_name"]
                        }
                        for real_name, alias_column in columns_map if real_name == sc["name"]
                    ]
                )

    return mapping
