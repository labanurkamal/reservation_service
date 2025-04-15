from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import api_v1_router
from core.config import settings
from dependencies.container import Container
from exceptions.base import AppException
from exceptions.handlers import app_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = Container()
    app.container = container

    yield
app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(api_v1_router, prefix='/api/v1')
