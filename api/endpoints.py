from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from services import user_service, transaction_service, coin_service
from schemas import UserCreate, TransactionCreate, UserResponse, TransactionResponse, CoinGenerationRequest
from utils import input_validation

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        await input_validation.validate_user_creation(user)
        return await user_service.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/transactions", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse
)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        await input_validation.validate_transaction_data(transaction)
        return await transaction_service.create_transaction(db, transaction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/coins/generate", response_model=List[TransactionResponse])
async def generate_coins(request: CoinGenerationRequest, db: Session = Depends(get_db)):
    try:
        await input_validation.validate_coin_generation(request)
        return await coin_service.generate_coins(db, request)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(user_id:int = Depends(user_service.get_current_user), db: Session = Depends(get_db)):
    try:
        return await user_service.get_user_by_id(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return await user_service.get_user_by_id(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    try:
        return await transaction_service.get_transaction_by_id(db, transaction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

```