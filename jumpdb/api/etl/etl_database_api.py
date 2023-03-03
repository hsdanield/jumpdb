from fastapi import Response, APIRouter

from fastapi import status

from jumpdb.serializers.etl_database_serial import ExtractLoadMappingIn, ExtractLoadMappingOut, ExtractSelectMapping, \
    OriginMapping
from jumpdb.service.etl.etl_database import exec_extract_load, extract_select

router = APIRouter()


@router.post("/extract_select", status_code=status.HTTP_200_OK, response_model=ExtractSelectMapping)
async def etl_extract_select(map_in: OriginMapping):
    print(map_in.select)

    result = extract_select(map_in)

    return result


@router.post("/extract_load", status_code=status.HTTP_201_CREATED, response_model=ExtractLoadMappingOut)
async def etl_extract_load(map_in: ExtractLoadMappingIn):
    result = exec_extract_load(origin=map_in.origin, destiny=map_in.destiny)

    return result
