from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database.models import User, Transaction
from schemas import TransactionResponse
from utils import input_validation

async def create_transaction(db: Session, transaction: TransactionCreate):
    try:
        await input_validation.validate_transaction_data(transaction)
        sender = db.query(User).filter(User.id == transaction.sender_id).first()
        recipient = db.query(User).filter(User.id == transaction.recipient_id).first()

        if not sender or not recipient:
            raise Exception("Sender or recipient not found")

        await input_validation.validate_transaction_amount(sender, transaction.amount)

        sender.balance -= transaction.amount
        recipient.balance += transaction.amount

        new_transaction = Transaction(sender_id=transaction.sender_id, recipient_id=transaction.recipient_id, amount=transaction.amount)
        db.add(new_transaction)
        db.commit()
        db.refresh(sender)
        db.refresh(recipient)
        return TransactionResponse.from_orm(new_transaction)
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating transaction: {e}")


async def get_transaction_by_id(db: Session, transaction_id: int):
    try:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if transaction:
            return TransactionResponse.from_orm(transaction)
        else:
            raise Exception("Transaction not found")
    except Exception as e:
        raise Exception(f"Error getting transaction by ID: {e}")


async def get_transaction_history(user_id: int, db: Session):
    try:
        transactions = db.query(Transaction).filter((Transaction.sender_id == user_id) | (Transaction.recipient_id == user_id)).all()
        history = [TransactionResponse.from_orm(transaction) for transaction in transactions]
        return history
    except Exception as e:
        raise Exception(f"Error getting transaction history: {e}")

async def process_transaction(sender_id: int, message: str, db: Session):
    try:
        sender_id, recipient_username, amount_str = message.split()
        amount = int(amount_str)
        return await process_transaction(sender_id,recipient_username,amount,db)
    except Exception as e:
        raise Exception(f"Error processing transaction message: {e}")

```