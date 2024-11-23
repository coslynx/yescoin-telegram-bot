from fastapi import APIRouter

from .app import router as admin_router

admin_router = APIRouter()
admin_router.include_router(admin_router)

```