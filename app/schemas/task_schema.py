from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title:str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class TaskRead(TaskBase):
    id:int

    class Config:
        from_attributes = True