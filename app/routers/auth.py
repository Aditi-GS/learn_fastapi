from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User
from ..schemas import Token, TokenData
from ..util import verify_password
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/token")
def login_for_access_token(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == userCredentials.username).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not verify_password(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    token_data = TokenData(user_id=user.id)
    token = create_access_token(data=token_data.model_dump())
    return Token(access_token=token, token_type="bearer")