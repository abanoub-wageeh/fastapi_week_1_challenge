from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
import schemas
from database import get_db
import models
import utils
import oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def create_user(user_data : schemas.UserCreate, db : Session = Depends(get_db)):
    user = db.exec(select(models.User).where(models.User.email == user_data.email)).first()
    print(user)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exist")
    new_user = models.User(**user_data.model_dump(exclude_unset=True))
    hashed_password = utils.hash_password(user_data.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    access_token = oauth2.create_access_token(
        {"user_id" : new_user.user_id,
        "email" : new_user.email})
    try:
        utils.send_verification_email(new_user.email, access_token)
        return {"message" : "check your email to verfiy your account"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="could not send the verfication email")



@router.get("/verify_account")
async def verfiy_user_account(token : str, db : Session = Depends(get_db) ):
    payload = oauth2.verify_access_token_sign_up(token)
    user = db.get(models.User, payload["user_id"])
    user.is_verified = True
    db.add(user)
    db.commit()
    return {"message" : "your account has been verifyed"}


@router.post("/login")
async def login(user_data : schemas.UserCreate, db : Session = Depends(get_db)):
    user = db.exec(select(models.User).where(models.User.email == user_data.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found, create an account")
    if not utils.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.is_verified != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified. Please verify your email to access this resource")
    access_token = oauth2.create_access_token({
        "user_id": user.user_id,
        "email": user.email,
        "role" : user.role,
        })
    refresh_token = oauth2.create_refresh_token({
        "user_id": user.user_id,
        "email": user.email,
        "role" : user.role,
        })
    user.refresh_token = refresh_token
    db.add(user)
    db.commit()
    return {"access_token" : access_token, "refresh_token" : refresh_token}

@router.post("/refresh")
async def refresh_token(token : str, db : Session = Depends(get_db)):
    payload = oauth2.verify_refresh_token(token, db)
    new_access_token = oauth2.create_access_token({"user_id": payload["user_id"], "email": payload["email"], "role": payload["role"]})
    return {"access_token": new_access_token}


@router.put("/revoke")
async def revoke_refresh_token(token : str, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.get_current_user)):
    user = db.get(models.User, user_credentials.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    user.refresh_token = None
    db.add(user)
    db.commit()
    return {"message": "logged out successfully, token revoked"}

