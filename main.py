from fastapi import FastAPI
from routes import notes, auth, admin, users
import database

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(notes.router)
app.include_router(users.router)

database.SQLModel.metadata.create_all(database.engine)

@app.get("/")
async def root():
    return {"message" : "hello in my notes website"}