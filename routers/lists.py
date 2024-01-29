from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.create_database import get_db

from ..schemas import list as schemas

from ..crud import list as crud
from ..crud import user as crud_user
from ..crud import relationship as crud_relationship



router = APIRouter(
    prefix="/lists",
    tags=["list"])


@router.post("/{user_id}/",response_model=schemas.List)
def create_list(user_id:int,list:schemas.ListCreate,db:Session = Depends(get_db)):
    db_user = crud_user.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return crud.create_list(db,list=list,user_id=user_id)

@router.get("/{user_id}/",response_model=list[schemas.List])
def get_lists(user_id:int,db:Session = Depends(get_db)):
    db_user = crud_user.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    return crud.get_user_lists(db,user_id=user_id)

@router.get("/single/{list_id}/")
def get_single_list(list_id:int, db:Session = Depends(get_db)):
    return crud.get_list(db,list_id=list_id)

@router.put("/{list_id}/",response_model=schemas.List)
def edit_list(list_id:int, list_edits:schemas.ListCreate, db: Session = Depends(get_db)):
    db_list = crud.get_list(db,list_id=list_id)
    if db_list is None:
        raise HTTPException(status_code=400, detail="List does not exist")
    return crud.edit_list(db,list_id = list_id, list_edits = list_edits)

#  returns user to list row
@router.post("/share/{list_id}/")
def share_list(list_id:int,user_email:str,db:Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db,user_email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist") 
    return crud.share_list(db,list_id=list_id,user_id=db_user.id)

@router.delete("/delete/{list_id}/")
def delete_list(list_id:int, db:Session = Depends(get_db)):
    return crud.delete_list_everywhere(db,list_id=list_id)

@router.delete("/{user_id}/{list_id}/")
def remove_list_from_user(user_id:int,list_id:int,db:Session = Depends(get_db)):

    if crud_relationship.count_users_for_list(db,list_id=list_id) < 2:
        raise HTTPException(status_code=400,detail="list only tied to one user. Must delete everywhere")
    return crud.remove_list_from_user(db,user_id=user_id,list_id=list_id)

