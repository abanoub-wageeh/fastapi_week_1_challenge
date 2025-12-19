from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
import models
import schemas
from datetime import datetime
import oauth2

router = APIRouter(tags=["admin endpoints"])

@router.get("/admin/notes", response_model=list[schemas.NoteResponse])
async def get_notes(db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.require_admin)):
    notes = db.exec(select(models.Note)).all()
    return notes

@router.get("/admin/notes/{note_id}", response_model=schemas.NoteResponse)
async def get_note_by_id(note_id : int, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.require_admin)):
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note not found")
    return note

@router.post("/admin/notes", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse)
async def create_note(note_data : schemas.NoteCreate, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.require_admin)):
    note = models.Note(**note_data.model_dump())
    note.owner_id = user_credentials.user_id
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/admin/notes/{note_id}", response_model=schemas.NoteResponse)
async def update_note(note_id : int, note_data : schemas.NoteUpdate, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.require_admin)):
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note not found")
    updated_data = note_data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(note, field, value)
    note.updated_at = datetime.now()
    db.commit()
    db.refresh(note)
    return note

@router.delete("/admin/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id : int, db : Session = Depends(get_db), user_credentials : schemas.UserResponse = Depends(oauth2.require_admin)):
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note that you are trying to delete does not exist")
    db.delete(note)
    db.commit()