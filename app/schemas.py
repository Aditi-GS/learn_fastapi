from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, List, Annotated
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
    pass

class PostUpdate(_PostRequestBase):
    pass

class PostResponse(_PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: _PostUserResponse
    model_config = ConfigDict(from_attributes=True)     # == orm_mode = True + Pydantic can read SQLAlchemy objects

class PostWithVotesResponse(BaseModel):
    Post: PostResponse
    votes: int
    model_config = ConfigDict(from_attributes=True)

class _PostOverview(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)

class UserPostsResponse(UserResponse):
    posts: List[_PostOverview]

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]