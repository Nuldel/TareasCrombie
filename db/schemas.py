from pydantic import BaseModel
from typing import Optional

class newTask(BaseModel):
    title: str
    description: Optional[str]
    state: str = 'Problemas'

    class Config:
        orm_mode = True
