from pydantic import BaseModel

class TaskBase(BaseModel):
    name: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskEdit(TaskBase):
    complete: bool

class Task(TaskBase):
    id: int
    complete: bool
    class Config:
        from_attribues = True