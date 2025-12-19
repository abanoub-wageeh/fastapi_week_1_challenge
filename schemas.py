from pydantic import BaseModel, Field, EmailStr
from datetime import datetime



class NoteCreate(BaseModel):
    title : str = Field(..., max_length=60, description="note title")
    content : str = Field(..., max_length=600, description="note content")


class NoteUpdate(BaseModel):
    title : str | None = Field(None, max_length=60)
    content : str | None = Field(None, max_length=600)

class NoteResponse(BaseModel):
    note_id : int
    title : str
    content : str
    owner_id : int
    created_at : datetime


class UserCreate(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8)


class UserUpdate(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8)



class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: str