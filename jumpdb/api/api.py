from jumpdb.api.routes.etl import etl_database

from fastapi import FastAPI

api = FastAPI()

api.include_router(etl_database.router, tags=['etl_database'])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("jumpdb.api.api:api", host="0.0.0.0", port=8000, reload=True)
