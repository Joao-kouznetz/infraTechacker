# query_service/schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenPayload(BaseModel):
    email: Optional[EmailStr] = None
    # sub: Optional[str] = None # Se usar 'sub' como subject (user_id)
    exp: Optional[int] = None


# Você pode adicionar outros schemas aqui se o query_service precisar deles
class UserDataFromToken(
    BaseModel
):  # Informações que você quer usar da validação do token
    email: EmailStr
    # user_id: Optional[str] = None # Se o token tiver user_id (sub)
