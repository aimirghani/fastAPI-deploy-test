from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post
from app import schemas
from app.security import oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])



@router.post("/", response_model=schemas.PostOutput)
def create_post(post_payload: schemas.PostInput, 
                db: Annotated[Session, Depends(get_db)],
                curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    new_post = Post(**post_payload.dict())
    new_post.owner_id = curr_user.id
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/", response_model=list[schemas.PostOutput])
def get_all_posts(db: Annotated[Session, Depends(get_db)],
            curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)],
            skip: int = 0, limit: int = 0):
    
    posts = db.query(Post).offset(offset=skip).limit(limit=limit).all()
    return posts


@router.get("/{id_}", response_model=schemas.PostOutput)
def get_post(id_: int, db: Annotated[Session, Depends(get_db)],
            curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    post = db.query(Post).get(id_)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id={id_}")
    return post


@router.put("/{id_}", response_model=schemas.PostOutput)
def get_post(id_: int, post_payload: schemas.PostInput,
            db: Annotated[Session, Depends(get_db)],
            curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    
    post_query = db.query(Post).filter_by(id=id_)
    
    post_to_edit = post_query.first()
    if not post_to_edit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id={id_}")
    if post_to_edit.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to edit posts that don't belong to you")
    
    post_query.update(post_payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id_: int, db: Annotated[Session, Depends(get_db)],
            curr_user: Annotated[schemas.UserOutput, Depends(oauth2.get_current_user)]):
    
    post_to_delete = db.query(Post).filter_by(id=id_).first()
    
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id={id_}")
    if post_to_delete.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to delete posts that don't belong to you")
    
    db.delete(post_to_delete)
    db.commit()
    
    return {"message": f"The post with id={id_} has been deleted successfully"}


