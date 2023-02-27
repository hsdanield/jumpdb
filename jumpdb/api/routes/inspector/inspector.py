from fastapi import Response, APIRouter, HTTPException
from fastapi import status

from typing import List

from jumpdb.serializers.inspector import (ColumnsIn,
                                          ColumnsOut,
                                          InspectorIn,
                                          ConstraintOut,
                                          FkConstraintOut,
                                          IndexConstraintOut,
                                          SummaryTableOut)

from jumpdb.service.inserpector.connection_service import (get_columns,
                                                           get_pk_constraint,
                                                           get_foreign_keys,
                                                           get_indexes,
                                                           get_summary_table,
                                                           mapping_column_type)

router = APIRouter()


@router.post("/columns", status_code=status.HTTP_200_OK, response_model=List[ColumnsOut])
async def columns(map_in: ColumnsIn):
    result = get_columns(map_in)

    return result


@router.post("/pks", status_code=status.HTTP_200_OK, response_model=ConstraintOut)
async def pks(map_in: InspectorIn):
    result = get_pk_constraint(map_in)

    return result


@router.post("/fks", status_code=status.HTTP_200_OK, response_model=List[FkConstraintOut])
async def fks(map_in: InspectorIn):
    result = get_foreign_keys(map_in)

    return result


@router.post("/indexes", status_code=status.HTTP_200_OK, response_model=List[IndexConstraintOut])
async def indexes(map_in: InspectorIn):
    result = get_indexes(map_in)

    return result


@router.post("/summary_table", status_code=status.HTTP_200_OK, response_model=SummaryTableOut)
async def summary_table(map_in: InspectorIn):
    result = get_summary_table(map_in)

    return result
