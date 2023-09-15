from fastapi import APIRouter
from app.api.endpoint import computation


api_router = APIRouter()

api_router.include_router(computation.router, tags=["computations"])
