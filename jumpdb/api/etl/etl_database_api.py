from fastapi import Response, APIRouter

from fastapi import status

from jumpdb.serializers.etl_database_serial import ExtLoadInMap, ExtLoadOutMap, ExtSltMap, \
    OriginMap
from jumpdb.service.etl.etl_database import exec_ext_load, ext_slt

router = APIRouter()


@router.post("/extract_select", status_code=status.HTTP_200_OK, response_model=ExtSltMap)
async def etl_extract_select(map_in: OriginMap):
    print(map_in.select)

    result = ext_slt(map_in)

    return result


@router.post("/extract_load", status_code=status.HTTP_201_CREATED, response_model=ExtLoadOutMap)
async def etl_extract_load(map_in: ExtLoadInMap):
    result = exec_ext_load(origin=map_in.origin, destiny=map_in.destiny)

    return result
