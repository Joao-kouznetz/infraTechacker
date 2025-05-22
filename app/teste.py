import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from pydantic import BaseModel, ValidationError

load_dotenv()  # Carrega as variáveis do .env
SALT = os.getenv("SALT")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    email: str
    exp: str


access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2FvLmJyZXNzZXJwZXJlaXJhQGdtYWlsLmNvbSIsImV4cCI6MTczMTAxMTY0OH0.UMhmXqP_ObI3KJiJuzg0kdxvuwqgzJxcZif9YFu5eQ4"
print(access_token)
payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
print(payload)
print(payload["exp"])
print(payload["sub"])
