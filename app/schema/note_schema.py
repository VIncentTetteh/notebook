from datetime import datetime

from app.schema.note_base_schema import NoteBase
from app.schema.user_schema import User

class Note(NoteBase):
    id: int
    created_at: datetime
    owner_id: int
    favourite: int
    owner: User

    class Config:
        orm_mode = True