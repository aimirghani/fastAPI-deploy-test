from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.models import User
from app.security import utils
from app.security import oauth2


router = APIRouter(prefix="/login", tags=["Authentication"])



@router.post("/")
def authenticate_user(user_payload: Annotated[OAuth2PasswordRequestForm, Depends()], 
                   db: Annotated[Session, Depends(get_db)]):
    
    CredentialsExeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    
    user = db.query(User).filter_by(email=user_payload.username).first()
    print(f"user object: {user}")
    if not user:
        raise CredentialsExeption
    if not utils.verify_password(user_payload.password, user.password):
        raise CredentialsExeption
    print(f"user object: {user}")
    token = oauth2.generate_access_token({"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}