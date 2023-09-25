from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqlalchemy import db
from jose import jwt
from pydantic import BaseModel, ValidationError

from models import Usuario
from security import SECRET_KEY, JWT_ALGORITHM

class TokenPayload(BaseModel):
    sub: Optional[int] = None

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login"
)

async def get_usuario_logado(
    token: str = Depends(reusable_oauth2)
) -> Usuario:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.session.query(Usuario).filter(Usuario.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user