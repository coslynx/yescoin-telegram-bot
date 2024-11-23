from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: int
    telegram_id: int
    username: str
    password_hash: str
    balance: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]


class Transaction(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    amount: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CoinGeneration(BaseModel):
    id: int
    user_id: int
    amount: int
    method: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(BaseModel):
    telegram_id: int
    username: str
    password_hash: str


class TransactionCreate(BaseModel):
    sender_id: int
    recipient_id: int
    amount: int


class CoinGenerationRequest(BaseModel):
    user_id: int
    amount: int
    method: str


class UserResponse(User):
    pass


class TransactionResponse(Transaction):
    pass

```