from pydantic import BaseModel

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    class Config:
        from_attribues = True