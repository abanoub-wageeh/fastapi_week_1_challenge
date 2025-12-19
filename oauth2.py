from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from database import get_db
import models
import schemas

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", )



def create_access_token(data : dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5)))
    to_encode.update({"type": "access","exp" : exp})
    access_token = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return access_token


def verify_access_token_sign_up(token : str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        if payload["type"] != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token" )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Link has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

def create_refresh_token(data: dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 15)))
    to_encode.update({"type": "refresh", "exp": exp})
    refresh_token = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return refresh_token

def verify_refresh_token(token : str, db : Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user = db.get(models.User, payload["user_id"])
        if not user or user.refresh_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Link has expired, you have to log in")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")



def get_current_user(token : str = Depends(oauth2_scheme)):
    payload = verify_access_token_sign_up(token)
    user = schemas.UserResponse(user_id=payload["user_id"], email=payload["email"], role=payload["role"])
    return user


def require_admin(user : schemas.UserResponse = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
    return user