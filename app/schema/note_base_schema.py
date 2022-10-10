from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str