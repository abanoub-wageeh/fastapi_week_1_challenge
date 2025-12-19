from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
import schemas
from database import get_db
import models
import utils
import oauth2

router = APIRouter(tags=["Users"])



@router.get("/users", response_model=list[schemas.UserResponse])
async def get_users(db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.get_current_user)):
    users = db.exec(select(models.User)).all()
    return users



@router.get("/myprofile", response_model=schemas.UserResponse)
async def get_my_profile(user_credentials : schemas.UserResponse = Depends(oauth2.get_current_user)):
    return user_credentials




@router.put("/user", response_model=schemas.UserResponse)
async def update_user(user_data : schemas.UserUpdate, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.get_current_user)):
    user = db.get(models.User, user_credentials.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    updated_data = user_data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(user, field, value)
    user.password = utils.hash_password(user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user




@router.delete("/user")
async def delete_user(user_credentials : schemas.UserResponse = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
    user = db.get(models.User, user_credentials.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    db.delete(user)
    db.commit()
    return {"message" : "user deleted successfully"}