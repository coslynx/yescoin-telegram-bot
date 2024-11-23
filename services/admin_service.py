from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import UserResponse, TransactionResponse, AdminActionRequest, AdminUserUpdateRequest
from models import User, Transaction
from utils import input_validation


async def get_all_users(db: Session = get_db):
    try:
        users = db.query(User).all()
        return [UserResponse.from_orm(user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_user_by_id(user_id: int, db: Session = get_db):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return UserResponse.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_user(user_id: int, request: AdminUserUpdateRequest, db: Session = get_db):
    try:
        await input_validation.validate_admin_user_update(request)
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.balance = request.balance if request.balance is not None else user.balance
            db.commit()
            db.refresh(user)
            return UserResponse.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def ban_user(user_id: int, db: Session = get_db):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Add ban logic here, perhaps adding a boolean field to User model.  
            #  This example just updates the balance for demonstration
            user.balance = 0
            db.commit()
            db.refresh(user)
            return UserResponse.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



async def unban_user(user_id: int, db: Session = get_db):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Remove ban logic here.  This example just updates the balance for demonstration.
            user.balance = 100 # Example - restore some balance
            db.commit()
            db.refresh(user)
            return UserResponse.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_all_transactions(db: Session = get_db):
    try:
        transactions = db.query(Transaction).all()
        return [TransactionResponse.from_orm(transaction) for transaction in transactions]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def perform_admin_action(request: AdminActionRequest, db: Session = get_db):
    try:
        await input_validation.validate_admin_action(request)
        if request.action == "ban":
            return await ban_user(request.user_id, db)
        elif request.action == "unban":
            return await unban_user(request.user_id, db)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

```