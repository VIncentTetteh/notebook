from typing import List, Optional
from .. import database, models, oauth2
from fastapi import APIRouter,status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schema import note_schema, note_create_schema
import logging
from app.logs.log_config_setup import setup_logging



router = APIRouter(tags=["Notes"], prefix="/notes")

setup_logging()
log = logging.getLogger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=note_schema.Note)
def create_note(note: note_create_schema.NoteCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_note = models.Note(owner_id=current_user.id, **note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    log.info(f"user {current_user.email} created note with title {note.title}")
    return new_note


@router.get("/", response_model=List[note_schema.Note])
def get_notes(db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,search: Optional[str]= ""):
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).filter(models.Note.title.contains(search)).limit(limit).all()
    log.info(f"user {current_user.email} viewed all notes")
    return notes

@router.get("/{id}", response_model=note_schema.Note, status_code=status.HTTP_404_NOT_FOUND)
def get_note(id:int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    note = db.query(models.Note).filter(models.Note.owner_id == current_user.id).filter(models.Note.id == id).first()

    if not note:
        log.error(f"note with id {id} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note with id {id} does not exist")

    log.info(f"user {current_user.email} search for note with title {note.title}")
    return note


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id:int, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.owner_id == current_user.id).filter(models.Note.id == id)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note with id {id} does not exist")

    note_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"note successfull deleted"}

@router.put("/{id}", response_model=note_schema.Note)
def update_note(id:int, note:note_create_schema.NoteCreate,db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note_to_update = note_query.first()
    if not note_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" note with id {id} does not exist")
    if note_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"unauthorized access")
    
    note_query.update(note.dict(), synchronize_session=False)
    db.commit()
    return note_query.first()

@router.patch("/{id}",response_model=note_schema.Note)
def patch_note(id:int,note:note_create_schema.NoteCreate, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note_to_patch = note_query.first()
    if not note_to_patch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" note with id {id} does not exist")

    if note_to_patch.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"note not found")
        
    note_data = note.dict(exclude_unset=True)
    note_query.update(note_data,synchronize_session=False)
    db.commit()
    return note_query.first()

@router.patch("/{id}", response_model=note_schema.Note)
def set_favourite(id:int, note:note_create_schema.NoteCreate, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note_to_patch = note_query.first()
    if not note_to_patch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note with id {id} does not exist")

    if note_to_patch.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"note not found")

    note_data = note.dict(exclude_unset=True)
    note_query.update(note_data, synchronize_session=False)
    db.commit()
    return note_query.first()






