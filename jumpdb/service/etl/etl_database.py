from jumpdb.repository.extract.extract_repository import ExtractRepository
from jumpdb.repository.load.load_repository import LoadRepository
from jumpdb.serializers.etl_database_serial import (OriginMap,
                                                    DestinyMap,
                                                    ExtLoadOutMap,
                                                    ExtSltMap,
                                                    ExtSltMapSaveFileIn,
                                                    ExtSltMapSaveFileOut,
                                                    FileMap)
from jumpdb.utils.file_util import write_csv, write_json
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


def ext_slt(origin: OriginMap):
    """EXTRACT - SELECT
     select no banco de dados ORIGEM
    """
    columns, values = __extract_select(database=origin.database,
                                       name=origin.name,
                                       stmt=origin.select)

    data = ExtSltMap(columns=columns, data=values, row_count=len(values))

    return data


def ext_slt_save_file(map_in: ExtSltMapSaveFileIn) -> ExtSltMapSaveFileOut:
    result = ext_slt(map_in.origin)
    is_write = __load_write_save_file(file_in=map_in.file, dict_data=result.data, columns=result.columns)

    return ExtSltMapSaveFileOut(is_write=is_write, format_file=map_in.file.format_file)


def __load_write_save_file(file_in: FileMap, dict_data, columns):
    is_write = False

    if file_in.format_file == "csv":
        is_write = write_csv(path_file=file_in.path_file, dict_data=dict_data, columns=columns)

    elif file_in.format_file == "json":
        is_write = write_json(path_file=file_in.path_file, dict_data=dict_data)

    return is_write


def exec_ext_load(origin: OriginMap, destiny: DestinyMap):
    """EXTRACT/LOAD: de uma tabela no banco de dados X (Atraves de select) para outra tabela no banco de dados Y
    """
    columns, values = __extract_select(database=origin.database,
                                       name=origin.name,
                                       stmt=origin.select)

    stmt_insert = create_query_insert(destiny.table, columns)

    row_count = __load_table(database=destiny.database,
                             name=destiny.name,
                             stmt=stmt_insert,
                             values=values)

    return ExtLoadOutMap(origin=origin, destiny=destiny, row_count=row_count)
