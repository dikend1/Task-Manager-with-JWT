from pydantic import BaseModel


class TaskBase(BaseModel):
    title:str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id:int

    class Config:
        from_attributes = True