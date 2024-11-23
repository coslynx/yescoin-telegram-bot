import bcrypt
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from database.models import User
from schemas import UserCreate, UserResponse
from utils import input_validation


async def create_user(db: Session, user: UserCreate):
    try:
        await input_validation.validate_user_creation(user)
        hashed_password = bcrypt.hashpw(user.password_hash.encode('utf-8'), bcrypt.gensalt())
        new_user = User(telegram_id=user.telegram_id, username=user.username, password_hash=hashed_password.decode('utf-8'))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.from_orm(new_user)
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {e}")


async def get_user(telegram_id: int, db: Session):
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            return UserResponse.from_orm(user)
        else:
            return None
    except Exception as e:
        raise Exception(f"Error getting user: {e}")


async def get_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return UserResponse.from_orm(user)
        else:
            raise Exception("User not found")
    except Exception as e:
        raise Exception(f"Error getting user by ID: {e}")


async def get_balance(telegram_id: int, db: Session):
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            return user.balance
        else:
            return 0
    except Exception as e:
        raise Exception(f"Error getting balance: {e}")


async def register_user(telegram_id: int, registration_data: str):
    try:
        username, password = registration_data.split()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = SessionLocal()
        new_user = User(telegram_id=telegram_id, username=username, password_hash=hashed_password.decode('utf-8'))
        db.add(new_user)
        db.commit()
        db.close()
        return True  # Registration successful
    except Exception as e:
        raise Exception(f"Error registering user: {e}")


async def get_current_user(telegram_id: int, db: Session):
    try:
        user = await get_user(telegram_id, db)
        if user:
            return user.id
        else:
            raise Exception("User not found")
    except Exception as e:
        raise Exception(f"Error getting current user: {e}")

async def update_user_balance(user_id: int, amount: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.balance += amount
            db.commit()
            db.refresh(user)
            return True
        else:
            raise Exception("User not found")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating user balance: {e}")

```