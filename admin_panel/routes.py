from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from services import admin_service
from schemas import AdminActionRequest, AdminUserUpdateRequest, UserResponse, TransactionResponse


router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        return await admin_service.get_all_users(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return await admin_service.get_user_by_id(user_id, db)
    except HTTPException as e:
        raise e  # Re-raise HTTPException for 404
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, request: AdminUserUpdateRequest, db: Session = Depends(get_db)):
    try:
        return await admin_service.update_user(user_id, request, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/users/{user_id}/actions", response_model=UserResponse)
async def perform_admin_action(user_id: int, request: AdminActionRequest, db: Session = Depends(get_db)):
    try:
        request.user_id = user_id
        return await admin_service.perform_admin_action(request, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_all_transactions(db: Session = Depends(get_db)):
    try:
        return await admin_service.get_all_transactions(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

```