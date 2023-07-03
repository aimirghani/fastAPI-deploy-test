from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.models import User
from app.security import utils, oauth2


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/", response_model=schemas.UserOutput)
def create_post(user_payload: schemas.UserInput, db: Annotated[Session, Depends(get_db)]):
    
    user = db.query(User).filter_by(email=user_payload.email).first()
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There is a user registered with this email already.")
    
    new_user = User(**user_payload.dict())
    new_user.password = utils.hash_password(user_payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/", response_model=schemas.UserOutputWithPosts)
def create_post(db: Annotated[Session, Depends(get_db)],
                curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    
    return curr_user