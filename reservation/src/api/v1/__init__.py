from fastapi import APIRouter

from .healthcheck import router as healthcheck_router
from .reservations import router as reservations_router
from .tables import router as tables_router

api_v1_router = APIRouter()

api_v1_router.include_router(healthcheck_router, prefix="/healthcheck", tags=["HEALTHCHECK"])
api_v1_router.include_router(tables_router, prefix="/tables", tags=["TABLES"])
api_v1_router.include_router(reservations_router, prefix="/reservations", tags=["RESERVATIONS"])
