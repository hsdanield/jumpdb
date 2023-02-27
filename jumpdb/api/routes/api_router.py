from fastapi import APIRouter
from jumpdb.api.routes.etl import etl_database
from jumpdb.api.routes.inspector import inspector

api_router = APIRouter()

api_router.include_router(etl_database.router, prefix="/etl/database", tags=['etl_database'])
api_router.include_router(inspector.router, prefix="/inspector/database", tags=['inspector'])
