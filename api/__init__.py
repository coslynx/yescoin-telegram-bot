from fastapi import APIRouter

from .endpoints import router as api_router

api_router = APIRouter()
api_router.include_router(api_router)
```