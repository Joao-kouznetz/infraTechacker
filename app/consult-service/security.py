# query_service/security.py
import jwt
from datetime import datetime, timezone
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
from schema import TokenPayload, UserDataFromToken  # Importe do seu schema.py local

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if (
                credentials.scheme.lower() != "bearer"
            ):  # Case-insensitive check for "Bearer"
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )


async def get_current_active_user(
    token: str = Depends(JWTBearer()),
) -> UserDataFromToken:
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = TokenPayload(**payload_dict)  # Valida o payload com Pydantic

        if payload.email is None:  # Ou payload.sub se estiver usando ID do usuário
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User identifier not in token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Aqui você pode popular UserDataFromToken. Se o token tivesse mais campos (ex: user_id),
        # você os extrairia aqui.
        return UserDataFromToken(email=payload.email)

    except jwt.ExpiredSignatureError:
        # Decodifica novamente sem verificar a expiração para obter a mensagem detalhada
        try:
            expired_payload_dict = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
            )
            exp_timestamp = expired_payload_dict.get("exp")
            if exp_timestamp:
                expired_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                time_since_expiration = datetime.now(timezone.utc) - expired_at
                expired_message = f"Token expired {time_since_expiration} ago at {expired_at.isoformat()}"
            else:
                expired_message = "Token expired, but expiration time is unavailable."
        except jwt.PyJWTError:  # Se não puder nem decodificar o token expirado
            expired_message = "Token is invalid or expired."

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=expired_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (
        jwt.PyJWTError
    ) as e:  # Outros erros de JWT (token inválido, assinatura errada, etc)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:  # Captura geral para erros inesperados durante a validação
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during token validation: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
