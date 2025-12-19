from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime

class Note(SQLModel, table=True):
    note_id : int | None = Field(default=None, primary_key=True)
    title : str = Field(max_length=60, nullable=False)
    content : str = Field(max_length=600, nullable=False)
    owner_id : int | None = Field(default=None, foreign_key="user.user_id", ondelete="CASCADE")
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)



class User(SQLModel, table=True):
    user_id : int | None = Field(default=None, primary_key=True)
    email : EmailStr = Field(unique=True, nullable=False)
    role : str = Field(default="user", nullable=False)
    password : str = Field(nullable=False)
    refresh_token : str | None = Field(default=None)
    is_verified : bool = Field(default=False)
    created_at : datetime = Field(default_factory=datetime.now)