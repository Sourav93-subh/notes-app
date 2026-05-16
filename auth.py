from jose import jwt
from datetime import datetime, timedelta
import hashlib

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# Hash Password
def hash_password(password: str):

    return hashlib.sha256(password.encode()).hexdigest()


# Verify Password
def verify_password(plain, hashed):

    return hashlib.sha256(plain.encode()).hexdigest() == hashed


# Create JWT Token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=10)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )