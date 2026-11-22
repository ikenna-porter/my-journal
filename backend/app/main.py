from fastapi import APIRouter, FastAPI

from app.routers import health

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    app = FastAPI(title="my-journal API", version="1.0.0")

    api = APIRouter(prefix=API_PREFIX)
    api.include_router(health.router)
    app.include_router(api)

    return app


app = create_app()
