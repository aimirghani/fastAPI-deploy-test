from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional



# ***************************** User **********************************

class UserBase(BaseModel):
    email: EmailStr


class UserInput(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime
    
    class Config:
        orm_mode = True


# ***************************** Post **********************************

class PostBase(BaseModel):
    title: str
    content: str


class PostInput(PostBase):
    published: Optional[bool] = True


class PostOutput(PostInput):
    id: int
    created_at: datetime
    owner: UserOutput
    
    class Config:
        orm_mode = True


class PostOutputInUser(PostInput):
    id: int
    
    class Config:
        orm_mode = True


class UserOutputWithPosts(UserOutput):
    posts: list[PostOutputInUser]

# ***************************** Token **********************************

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int