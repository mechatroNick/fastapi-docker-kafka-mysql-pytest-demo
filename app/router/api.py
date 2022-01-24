from fastapi import APIRouter
from .v1 import customers, items, healthcheck

api_router = APIRouter()
api_router.include_router(customers.router, prefix="/customers")
api_router.include_router(items.router, prefix="/items")
api_router.include_router(healthcheck.router, prefix="/healthcheck")
