from fastapi import APIRouter

from api.chat import router as chat_router

router = APIRouter()

router.include_router(prefix='/chat', router=chat_router, tags=['bot'])
