import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from .models import User
from .config import settings

# to get a string like this run: openssl rand -hex 32
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes

# tokenUrl == Authentication Endpoint (in our case = /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        id = int(payload.get("user_id"))
        if not id: 
            raise credentials_exceptions
        token_data = TokenData(user_id=id)
    except InvalidTokenError:
        raise credentials_exceptions
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token=token, credentials_exceptions=credentials_exceptions)
    if not token_data.user_id:
        raise credentials_exceptions
    
    user = db.query(User).filter(User.id == token_data.user_id).one_or_none()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No user {token_data.user_id} found")
    return user