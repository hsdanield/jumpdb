from typing import List, Optional

from fastapi import FastAPI, Response, status
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, validator

from jumpdb.repository.extract.extract_repository import DatasourceConnection, OriginDatabaseRepository, \
    DestinyDatabaseRepository, ContractDatabaseRepository


class EtlDatabaseOut(BaseModel):
    name_origin: str
    name_destiny: str
    type_origin: str
    type_destiny: str
    select: str
    table_destiny: str
    row_count: int


class EtlDatabaseIn(BaseModel):
    name_origin: str
    name_destiny: str
    type_origin: str
    type_destiny: str
    select: str
    table_destiny: str


api = FastAPI(title="ETL DATABASES")


@api.post("/etl_database", response_model=EtlDatabaseOut)
async def etl_database(etl: EtlDatabaseIn, response: Response):
    conn_origin = DatasourceConnection(database=etl.type_origin, name=etl.name_origin)
    conn_destiny = DatasourceConnection(database=etl.type_destiny, name=etl.name_destiny)
    origin = OriginDatabaseRepository(ds_connection=conn_origin)
    destiny = DestinyDatabaseRepository(ds_connection=conn_destiny)
    contract = ContractDatabaseRepository(origin_connection=origin, destiny_connection=destiny)
    columns, values = contract.select_origin(etl.select)
    row_count = contract.insert_destiny(table=etl.table_destiny, columns=columns, values=values)

    response.status_code = status.HTTP_201_CREATED

    return EtlDatabaseOut(
        name_origin=etl.name_origin,
        name_destiny=etl.name_destiny,
        type_origin=etl.type_origin,
        type_destiny=etl.type_destiny,
        select=etl.select,
        table_destiny=etl.table_destiny,
        row_count=row_count
    )
