from fastapi import FastAPI

from jumpdb.api.routes.etl import etl_database
from jumpdb.api.routes.inspector import inspector

api = FastAPI()

api.include_router(etl_database.router, tags=['etl_database'])
api.include_router(inspector.router, tags=['inspector'])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("jumpdb.api.api:api", host="0.0.0.0", port=8000, reload=True)
