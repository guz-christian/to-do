
from pydantic import BaseModel

class TaskToListBase(BaseModel):
    task_id: int
    list_id: int

class TaskToListEdit(TaskToListBase):
    pass

class TaskToList(TaskToListBase):
    id: int
    class Config:
        from_attribues = True

class ListToUser(BaseModel):
    id: int
    list_id: int
    user_id: int

    class Config:
        from_attribues = True
