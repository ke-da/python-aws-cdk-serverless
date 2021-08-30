from fastapi import APIRouter

from .endpoints import routes
router = APIRouter()


router.include_router(routes.router, prefix="/test", tags=["Endpoint Test"])