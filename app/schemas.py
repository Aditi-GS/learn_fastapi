from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
class _UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreate(_UserCredentials):
    pass    

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class _PostUserResponse(BaseModel):
    id: int
    email: EmailStr

class _PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class _PostRequestBase(_PostBase):
    model_config = ConfigDict(extra="forbid")   # can't pass id and created_at => generated at run time

class PostCreate(_PostRequestBase):
    rating: Optional[int] = None

# can't update rating
class PostUpdate(_PostRequestBase):
    pass

class PostResponse(_PostBase):
    id: int
    rating: Optional[int] = None
    created_at: datetime
    user_id: int
    user: _PostUserResponse
    model_config = ConfigDict(from_attributes=True)     # == orm_mode = True + Pydantic can read SQLAlchemy objects

class _PostOverview(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)

class UserPostsResponse(UserResponse):
    posts: List[_PostOverview]