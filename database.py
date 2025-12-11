from sqlmodel import create_engine, SQLModel, Session, Field
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Note(SQLModel, table=True):
    note_id : int = Field(primary_key=True)
    title : str = Field(max_length=60, nullable=False)
    content : str = Field(max_length=600, nullable=False)
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)


engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    with Session(engine) as db:
        yield db