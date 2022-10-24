from typing import Union
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: Union[str,None]
    content: Union[str,None]
    favourite: Union[int,None]