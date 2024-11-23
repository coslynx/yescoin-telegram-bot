import bcrypt

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        The bcrypt-hashed password.

    Raises:
        TypeError: if password is not a string.
        ValueError: if password is empty.

    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not password:
        raise ValueError("Password cannot be empty.")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Checks if a password matches a bcrypt-hashed password.

    Args:
        password: The password to check.
        hashed_password: The bcrypt-hashed password.

    Returns:
        True if the password matches, False otherwise.

    Raises:
        TypeError: if password or hashed_password is not a string.
        ValueError: if password or hashed_password is empty.

    """
    if not isinstance(password, str) or not isinstance(hashed_password, str):
        raise TypeError("Password and hashed password must be strings.")
    if not password or not hashed_password:
        raise ValueError("Password and hashed password cannot be empty.")
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

```