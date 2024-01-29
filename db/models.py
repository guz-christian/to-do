from sqlalchemy import Boolean, Column, Integer, String
from .create_database import Base
from sqlalchemy.orm import relationship

class TaskToUser(Base):
    __tablename__ = "task_to_user"

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    task_id = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)

class ListToUser(Base):
    __tablename__ = "list_to_user"

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    list_id = Column(Integer)

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer,primary_key=True)
    name = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True)

    name = Column(String)
    description = Column(String)

    complete = Column(Boolean,default=False)
    
class TaskToList(Base):
    __tablename__ = "task_to_list"

    id = Column(Integer,primary_key=True)
    task_id = Column(Integer)
    list_id = Column(Integer)
