from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import Header, APIRouter, Depends

from services.dependencies.containers import Application
from services.dependencies.services import RedisService
from services.misc.schemas import TestResponse, User
from services.utils.security import get_current_user

api_router = APIRouter(prefix="/api_v1/v1")


@api_router.post("/test", tags=["Test"], response_model=TestResponse)
@api_router.get("/test", tags=["Test"], response_model=TestResponse)
@inject
async def test(
        user: User = Depends(get_current_user),
        user_agent: Optional[str] = Header(...),
        service: RedisService = Depends(Provide[Application.services.redis_]),
):
    """ Test query """
    value = await service.cache_process('cached_', 1, expire=40)
    return {"success": True, "User-Agent": user_agent, "value": value}