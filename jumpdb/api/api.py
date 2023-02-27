from fastapi import FastAPI

from jumpdb.api.routes.api_router import api_router

api = FastAPI(title="jumpdb API")
api.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("jumpdb.api.api:api", host="0.0.0.0", port=8000, reload=True)
