from operator import contains
from turtle import title
from typing import List, Optional
from .. import database, models, schemas, oauth2
from fastapi import APIRouter,status, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Notes"], prefix="/notes")

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    current_user: int = Depends(oauth2.get_current_user)
    new_note = models.Note(owner_id=current_user.id, **note.dict())
    db.add(new_note)
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=List[schemas.Note])
def get_router(db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.oauth2.get_current_user), limit: int = 10,search: Optional[str]= ""):
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).filter(models.Note.title.contains(search)).limit(limit).all()
    return notes




