from fastapi import Response, APIRouter

from fastapi import status

from jumpdb.serializers.etl_database import ExtractLoadMappingIn, ExtractLoadMappingOut
from jumpdb.service.etl.etl_database import exec_extract_load

router = APIRouter()


@router.post("/api/v1/etl-database", response_model=ExtractLoadMappingOut)
async def etl_database(map_in: ExtractLoadMappingIn, response: Response):
    result = exec_extract_load(origin=map_in.origin,
                               destiny=map_in.destiny)

    response.status_code = status.HTTP_201_CREATED

    return result
