from typing import List

from jumpdb.repository.datasource.datasource_connection import DatasourceConnection
from jumpdb.repository.inspect_repository import DatasourceInspect
from jumpdb.serializers.inspector_serial import (InspectorIn,
                                                 ColumnsIn, ColumnsOut,
                                                 FkConstraintOut, IndexConstraintOut,
                                                 ConstraintOut, SummaryTableOut)


def __create_inspector(database, name):
    inspector = None
    try:
        connection = DatasourceConnection(database, name)
        inspector = DatasourceInspect(connection)
    except Exception as e:
        print(f"Ops! Erro em create_inspector: {e}")

    return inspector


def get_columns(map_in: ColumnsIn) -> List[ColumnsOut]:
    map_out = None

    try:

        inspector = __create_inspector(database=map_in.database, name=map_in.name)
        data = inspector.get_columns(map_in.table_name, map_in.filter_columns)

        map_out = [ColumnsOut(**item) for item in data]

    except Exception as e:
        print(f"Ops! Erro em get_columns: {e}")

    return map_out


def get_pk_constraint(map_in: InspectorIn) -> ConstraintOut:
    map_out = None
    try:
        inspector = __create_inspector(map_in.database, map_in.name)
        data = inspector.get_pk_constraint(table_name=map_in.table_name)

        map_out = ConstraintOut(database=map_in.database,
                                name=map_in.name,
                                table_name=map_in.table_name,
                                constraint_name=data["name"],
                                constrained_columns=data["constrained_columns"]
                                )

    except Exception as e:
        print(f"Ops! Erro em get_pk_constraint: {e}")

    return map_out


def get_foreign_keys(map_in: InspectorIn) -> List[FkConstraintOut]:
    map_out_list = []
    try:
        inspector = __create_inspector(map_in.database, map_in.name)
        data = inspector.get_foreign_keys(table_name=map_in.table_name)

        for item in data:
            constraint_out = ConstraintOut(database=map_in.database,
                                           name=map_in.name,
                                           table_name=map_in.table_name,
                                           constraint_name=item["name"],
                                           constrained_columns=item["constrained_columns"]
                                           )
            fk = FkConstraintOut(constraint_out=constraint_out,
                                 referred_schema=item["referred_schema"],
                                 referred_table=item["referred_table"],
                                 referred_columns=item["referred_columns"],
                                 options=item["options"])

            map_out_list.append(fk)

    except Exception as e:
        print(f"Ops! Erro em get_foreign_keys: {e}")

    return map_out_list


def get_indexes(map_in: InspectorIn) -> List[IndexConstraintOut]:
    map_out_list = []
    try:
        inspector = __create_inspector(map_in.database, map_in.name)
        data = inspector.get_indexes(table_name=map_in.table_name)

        for item in data:
            constraint_out = ConstraintOut(
                database=map_in.database,
                name=map_in.name,
                table_name=map_in.table_name,
                constraint_name=item["name"],
                constrained_columns=item["column_names"]
            )

            index_out = IndexConstraintOut(constraint_out=constraint_out,
                                           index_name=item["name"],
                                           dialect_options=item["dialect_options"],
                                           unique=item["unique"])

            map_out_list.append(index_out)

    except Exception as e:
        print(f"Ops! Erro em get_indexes: {e}")

    return map_out_list


def get_summary_table(map_in: InspectorIn) -> SummaryTableOut:
    columns_in = ColumnsIn(database=map_in.database, name=map_in.name, table_name=map_in.table_name,
                           filter_columns=None)

    columns_out = get_columns(columns_in)
    constraint_out = get_pk_constraint(map_in)
    fk_out = get_foreign_keys(map_in)
    index_out = get_indexes(map_in)

    summary = SummaryTableOut(columns_out=columns_out,
                              constraint_out=constraint_out,
                              fk_out=fk_out,
                              index_out=index_out)

    return summary


def mapping_column_type(database, name, content):
    mapping = []
    columns_map = []
    #
    # i = 0
    # data = get_tables_and_columns(content)["data"]
    # for item in data:
    #     table = item[0]["table"]
    #     columns = item[1]["columns"]
    #
    #     if columns:
    #
    #         columns_map = [(column["real_name"], column["alias_column"]) for column in columns if column]
    #
    #         searchcolumns = get_columns(database=database,
    #                                     name=name,
    #                                     table_name=table["real_name"],
    #                                     filter_columns=sorted([column[0] for column in columns_map if columns]))
    #         for sc in searchcolumns:
    #             mapping.append(
    #                 *[
    #                     {
    #                         "real_name": real_name,
    #                         "alias_column": alias_column,
    #                         "precision": sc["precision"],
    #                         "table_name": table["real_name"]
    #                     }
    #                     for real_name, alias_column in columns_map if real_name == sc["name"]
    #                 ]
    #             )

    return mapping
