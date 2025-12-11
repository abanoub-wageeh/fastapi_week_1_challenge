from fastapi import FastAPI
from routes import notes
import database

app = FastAPI()

app.include_router(notes.router)

database.SQLModel.metadata.create_all(database.engine)

@app.get("/")
async def root():
    return {"message" : "hello in my notes website"}