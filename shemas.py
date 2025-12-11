from pydantic import BaseModel, Field
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
    created_at : datetime

