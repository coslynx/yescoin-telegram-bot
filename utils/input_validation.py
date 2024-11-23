import bcrypt
from sqlalchemy.orm import Session
from schemas import UserCreate, TransactionCreate, CoinGenerationRequest
from database.models import User

async def validate_registration(registration_data: str):
    try:
        username, password = registration_data.split()
        if not username or not password:
            raise ValueError("Username and password are required.")
        if len(username) < 5 or len(username) > 20:
            raise ValueError("Username must be between 5 and 20 characters.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

    except ValueError as e:
        raise ValueError(f"Invalid registration data: {e}")


async def validate_user_creation(user: UserCreate):
    if not user.username or not user.password_hash or not user.telegram_id:
        raise ValueError("Username, password, and Telegram ID are required.")
    if len(user.username) < 5 or len(user.username) > 20:
        raise ValueError("Username must be between 5 and 20 characters.")
    if len(user.password_hash) < 8:
        raise ValueError("Password must be at least 8 characters.")
    hashed_password = bcrypt.hashpw(user.password_hash.encode('utf-8'), bcrypt.gensalt())
    user.password_hash = hashed_password.decode('utf-8')


async def validate_transaction(transaction_data: str):
    try:
        sender_id, recipient_username, amount_str = transaction_data.split()
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not recipient_username:
            raise ValueError("Recipient username is required.")

    except ValueError as e:
        raise ValueError(f"Invalid transaction data: {e}")


async def validate_transaction_data(transaction: TransactionCreate):
    if not transaction.sender_id or not transaction.recipient_id or not transaction.amount:
        raise ValueError("Sender ID, recipient ID, and amount are required.")
    if transaction.amount <= 0:
        raise ValueError("Amount must be positive.")


async def validate_transaction_amount(sender: User, amount: int):
    if sender.balance < amount:
        raise ValueError("Insufficient funds.")


async def validate_coin_generation(request: CoinGenerationRequest):
    if not request.user_id or not request.amount or not request.method:
        raise ValueError("User ID, amount, and method are required.")
    if request.amount <= 0:
        raise ValueError("Amount must be positive.")


async def validate_admin_user_update(request: AdminUserUpdateRequest):
    if request.balance is not None and request.balance < 0:
        raise ValueError("Balance cannot be negative.")


async def validate_admin_action(request: AdminActionRequest):
    if not request.user_id or not request.action:
        raise ValueError("User ID and action are required.")
    if request.action not in ["ban", "unban"]:
        raise ValueError("Invalid action.")

```