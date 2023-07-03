from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app import database, models, schemas



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def generate_access_token(payload_dict):
    data_to_encode = payload_dict.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    data_to_encode.update({"exp": expire})
    
    jwt_token = jwt.encode(data_to_encode, 
                       key=settings.secret_key, 
                       algorithm=settings.algorithm)
    
    return jwt_token



def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db: Annotated[Session, Depends(database.get_db)]):
    
    CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        token_payload = jwt.decode(token=token, 
                                    key=settings.secret_key, 
                                    algorithms=settings.algorithm)
        user_id = token_payload.get("user_id")
        if not user_id:
            raise CredentialsException
    except JWTError:
        raise CredentialsException
    
    token_data = schemas.TokenData(user_id=user_id)
    
    user = db.query(models.User).get(token_data.user_id)
    
    return user