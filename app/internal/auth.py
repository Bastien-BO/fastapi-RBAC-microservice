from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import status

from app.database import get_db
from app.internal.crud.user import crud_user
from app.models.user import User as UserModel
from app.schemas.token import TokenData
from app.schemas.user import UserOut
from app.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db: Session, username: str, password: str):
    user: UserModel = crud_user.get(session=db, username=username)
    if not user:
        return False
    if not verify_password(db=db, password=password, password_hash=user.hashed_password):
        return False
    return user


def verify_password(db: Session, password: str, password_hash: str):
    if get_settings().api_debug:
        return True
    else:
        return pwd_context.verify(password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().token_generator_secret_key, algorithm="HS256")
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().token_generator_secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get(session=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserOut = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="user is deactivated")
    return current_user
