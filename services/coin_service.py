from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database.models import User, Transaction, CoinGeneration
from schemas import TransactionResponse
from utils import input_validation

async def generate_coins(db: Session, request: CoinGenerationRequest):
    try:
        await input_validation.validate_coin_generation(request)
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise Exception("User not found")

        new_coins = request.amount
        user.balance += new_coins
        new_transaction = Transaction(sender_id=0, recipient_id=request.user_id, amount=new_coins)
        db.add(new_transaction)

        new_coin_generation = CoinGeneration(user_id=request.user_id, amount=new_coins, method=request.method)
        db.add(new_coin_generation)
        db.commit()
        db.refresh(user)
        return [TransactionResponse.from_orm(new_transaction)]


    except Exception as e:
        db.rollback()
        raise Exception(f"Error generating coins: {e}")

async def get_user_balance(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.balance
        else:
            return 0  # or raise exception
    except Exception as e:
        raise Exception(f"Error getting balance: {e}")

async def get_transaction_history(user_id: int, db: Session):
    try:
        transactions = db.query(Transaction).filter((Transaction.sender_id == user_id) | (Transaction.recipient_id == user_id)).all()
        history = [TransactionResponse.from_orm(transaction) for transaction in transactions]
        return history
    except Exception as e:
        raise Exception(f"Error getting transaction history: {e}")

async def process_transaction(sender_id: int, recipient_username:str, amount:int, db: Session):
    try:
        sender = db.query(User).filter(User.id == sender_id).first()
        recipient = db.query(User).filter(User.username == recipient_username).first()

        if not sender or not recipient:
            raise Exception("Sender or recipient not found")
        
        await input_validation.validate_transaction_amount(sender,amount)


        sender.balance -= amount
        recipient.balance += amount

        new_transaction = Transaction(sender_id=sender_id, recipient_id=recipient.id, amount=amount)
        db.add(new_transaction)
        db.commit()
        db.refresh(sender)
        db.refresh(recipient)
        return new_transaction
    except Exception as e:
        db.rollback()
        raise Exception(f"Error processing transaction: {e}")


```