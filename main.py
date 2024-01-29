from fastapi import FastAPI, Depends
# from .db.create_database import engine

from .routers import users, lists, tasks
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from .db.create_database import get_db
from .db import models
from .schemas import relationship as schemas
from .schemas import task as task_schemas


# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router) 
app.include_router(lists.router) 
app.include_router(tasks.router)