from fastapi import Response, APIRouter

from fastapi import status

from jumpdb.serializers.etl_database_serial import ExtractLoadMappingIn, ExtractLoadMappingOut
from jumpdb.service.etl.etl_database import exec_extract_load

router = APIRouter()


@router.post("/extract_load", status_code=status.HTTP_201_CREATED, response_model=ExtractLoadMappingOut)
async def etl_database(map_in: ExtractLoadMappingIn):
    result = exec_extract_load(origin=map_in.origin, destiny=map_in.destiny)

    return result
