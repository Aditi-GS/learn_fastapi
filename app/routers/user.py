from fastapi import status, HTTPException, Depends, APIRouter
from ..schemas import UserCreate, UserResponse, UserPostsResponse
from ..models import User
from ..util import get_password_hash
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())
    hashed_password = get_password_hash(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}", response_model=UserPostsResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).one_or_none()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No such user with id = {id} bruv :/")
    return user