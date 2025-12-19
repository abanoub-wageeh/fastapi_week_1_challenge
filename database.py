from sqlmodel import create_engine,SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as db:
        yield db