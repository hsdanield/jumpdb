from fastapi import Response, APIRouter
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


@router.post("/inspector/database/columns", response_model=List[ColumnsOut])
async def columns(map_in: ColumnsIn, response: Response):
    result = get_columns(map_in)

    # response.status_code = status.HTTP_200_OK

    return result


@router.post("/inspector/database/pks", response_model=ConstraintOut)
async def pks(map_in: InspectorIn, response: Response):
    result = get_pk_constraint(map_in)

    return result


@router.post("/inspector/database/fks", response_model=List[FkConstraintOut])
async def fks(map_in: InspectorIn, response: Response):
    result = get_foreign_keys(map_in)

    return result


@router.post("/inspector/database/indexes", response_model=List[IndexConstraintOut])
async def indexes(map_in: InspectorIn, response: Response):
    result = get_indexes(map_in)

    return result


@router.post("/inspector/database/summary_table", response_model=SummaryTableOut)
async def summary_table(map_in: InspectorIn, response: Response):
    result = get_summary_table(map_in)

    return result
