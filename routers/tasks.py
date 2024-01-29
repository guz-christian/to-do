from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.create_database import get_db

from ..schemas import task as schemas
from ..schemas import relationship as schemas_relationship
from ..crud import task as crud
from ..crud import list as crud_list
from ..crud import relationship as crud_relationship

router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)

@router.post("/{list_id}/",response_model=schemas.Task)
def create_task(task:schemas.TaskCreate,list_id:int,db:Session = Depends(get_db)):
    return crud.create_task(db,task,list_id=list_id)

@router.get("/single/{task_id}/", response_model=schemas.Task)
def get_single_task(task_id:int, db:Session = Depends(get_db)):
    return crud.get_single_task(db, task_id=task_id)

@router.get("/all/", response_model=list[schemas.Task])
def get_all_tasks(db:Session = Depends(get_db)):
    return crud.get_all_tasks(db=db)

@router.get("/{list_id}/",response_model=list[schemas.Task])
def get_list_tasks(list_id:int, db:Session = Depends(get_db)):
    db_list = crud_list.get_list(db,list_id=list_id)
    if db_list is None:
        raise HTTPException(status_code=400,detail="list does not exist")
    return crud.get_list_tasks(db, list_id)

@router.put("/edit/{task_id}/", response_model=schemas.Task)
def edit_task(task_id:int,task:schemas.Task, db:Session = Depends(get_db)):
    db_task = crud.get_single_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=400, detail="task does not exist")
    return crud.edit_task(db,task=task,task_id=task_id)

@router.post("/share/{task_id}/")
def share_task(task_id:int, list_id:int, db:Session = Depends(get_db)):
    return crud_relationship.add_task_list_row(db,task_id=task_id,list_id=list_id)

@router.put("/move/{list_origin_id}/", response_model=schemas_relationship.TaskToList)
def move_task(list_origin_id:int, task_list_row: schemas_relationship.TaskToListEdit,db:Session = Depends(get_db)):
    return crud_relationship.move_task_to_list(db, list_origin_id=list_origin_id, task_list_row=task_list_row)
    # return crud.move_task(db,list_origin_id = list_origin_id,task_list_row=task_list_row)

@router.delete("/{task_id}/")
def delete_task(task_id:int,db:Session = Depends(get_db)):
    return crud.delete_task_everywhere(db,task_id=task_id)

@router.delete("/{task_id}/{list_id}/")
def remove_task_from_list(task_id:int,list_id:int,db:Session = Depends(get_db)):

    if crud_relationship.count_lists_for_task(db,task_id=task_id) < 2:
        raise HTTPException(status_code=400,detail="task only in one list. Must delete everywhere")
    return crud.remove_task_from_list(db,task_id=task_id,list_id=list_id)

