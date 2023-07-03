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
    created_at: datetime
    
    class Config:
        orm_mode = True


# ***************************** Post **********************************

class PostBase(BaseModel):
    title: str
    content: str


class PostInput(PostBase):
    published: Optional[bool] = None


class PostOutput(PostInput):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True


# ***************************** Token **********************************

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int