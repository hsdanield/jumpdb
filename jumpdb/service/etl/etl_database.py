from jumpdb.repository.extract.extract_repository import ExtractRepository
from jumpdb.repository.load.load_repository import LoadRepository
from jumpdb.serializers.etl_database_serial import (OriginMapping,
                                                    DestinyMapping,
                                                    ExtractLoadMappingOut,
                                                    ExtractSelectMapping)
from jumpdb.utils.sql_parser_util import create_query_insert


def __extract_select(database, name, stmt):
    columns = None
    values = None

    extract_repository = ExtractRepository(database, name)

    if extract_repository.check_connection():
        columns, values = extract_repository.select(stmt)

    return columns, values


def __load_table(database, name, stmt, values) -> int:
    data = None

    load_repository = LoadRepository(database, name)

    if load_repository.check_connection():
        data = load_repository.insert(stmt, values)

    return data


def extract_select(origin: OriginMapping):
    columns, values = __extract_select(database=origin.database,
                                       name=origin.name,
                                       stmt=origin.select)

    data = ExtractSelectMapping(columns=columns, data=values, row_count=len(values))

    return data


def exec_extract_load(origin: OriginMapping, destiny: DestinyMapping):
    columns, values = __extract_select(database=origin.database,
                                       name=origin.name,
                                       stmt=origin.select)

    stmt_insert = create_query_insert(destiny.table, columns)

    row_count = __load_table(database=destiny.database,
                             name=destiny.name,
                             stmt=stmt_insert,
                             values=values)

    return ExtractLoadMappingOut(origin=origin, destiny=destiny, row_count=row_count)
