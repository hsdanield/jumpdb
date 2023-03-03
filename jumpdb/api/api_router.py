from fastapi import APIRouter
from jumpdb.api.inspector import inspector_api
from jumpdb.api.etl import etl_database_api

api_router = APIRouter()

api_router.include_router(etl_database_api.router, prefix="/etl/database", tags=['etl_database'])
api_router.include_router(inspector_api.router, prefix="/inspector/database", tags=['inspector'])
