from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    hashed_password: str
    class Config:
        from_attribues = True