from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session,select
from database import get_db, Note
import shemas
from datetime import datetime


router = APIRouter(tags=["notes"])

@router.get("/notes", response_model=list[shemas.NoteResponse])
async def get_notes(db : Session = Depends(get_db)):
    notes = db.exec(select(Note)).all()
    return notes

@router.get("/notes/{note_id}", response_model=shemas.NoteResponse)
async def get_note_by_id(note_id : int, db : Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note not found")
    return note

@router.post("/note", status_code=status.HTTP_201_CREATED, response_model=shemas.NoteResponse)
async def create_note(note_data : shemas.NoteCreate, db : Session = Depends(get_db)):
    note = Note(**note_data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/notes/{note_id}", response_model=shemas.NoteResponse)
async def update_note(note_id : int, note_data : shemas.NoteUpdate, db : Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note not found")
    updated_data = note_data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(note, field, value)
    note.updated_at = datetime.now()
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}")
async def delete_note(note_id : int, db : Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note that you are trying to delete does not exist")
    db.delete(note)
    db.commit()
    return {"message" : "note has been deleted succufully"}