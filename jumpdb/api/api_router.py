from fastapi import APIRouter
from jumpdb.api.inspector import inspector_api
from jumpdb.api.etl.etl_database_api import etl_database

api_router = APIRouter()

api_router.include_router(etl_database.router, prefix="/etl/database", tags=['etl_database'])
api_router.include_router(inspector_api.router, prefix="/inspector/database", tags=['inspector'])
