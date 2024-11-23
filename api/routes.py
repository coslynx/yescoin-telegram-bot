from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services import user_service, transaction_service
from schemas import UserCreate, TransactionCreate


router = APIRouter(prefix="/api", tags=["api"])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return await user_service.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/transactions", status_code=status.HTTP_201_CREATED, response_model=TransactionCreate)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return await transaction_service.create_transaction(db, transaction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

```