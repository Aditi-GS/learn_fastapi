from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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
    model_config = ConfigDict(from_attributes=True)     # == orm_mode = True