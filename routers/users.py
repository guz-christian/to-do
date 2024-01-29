from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.create_database import get_db

from ..schemas import user as schemas
from ..crud import user as crud

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/",response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db,user)

@router.get("/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100,db:Session = Depends(get_db)):
    return crud.get_users(db,skip=skip,limit=limit)

@router.get("/{user_email}/",response_model=schemas.User)
def get_user(user_email: str,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,user_email)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return db_user
