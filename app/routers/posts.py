from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post
from app import schemas, oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])



@router.post("/")
def create_post(post_payload: schemas.PostInput, 
                db: Annotated[Session, Depends(get_db)],
                curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    new_post = Post(**post_payload.dict())
    new_post.owner_id = curr_user.id
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post