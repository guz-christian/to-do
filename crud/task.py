
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import task as schemas
from ..schemas import relationship as schemas_relationship

from . import relationship

def create_task(db:Session,task:schemas.TaskCreate,list_id:int):
    db_task = models.Task(name = task.name,description = task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    relationship.add_task_list_row(db,task_id=db_task.id,list_id=list_id)
    return db_task

def get_single_task(db:Session,task_id:int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def edit_task(db:Session,task_id:int,task:schemas.Task):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.complete = task.complete
    db_task.name = task.name
    db_task.description = task.description

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def toggle_task_complete(db:Session,task_id):
    db_task = get_single_task(db, task_id=task_id)
    if db_task.complete == True:
        db_task.complete = False
    else:
        db_task.complete = True
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db:Session):
    return db.query(models.Task).all()

def get_list_tasks(db:Session,list_id:int):
    tasks = []
    db_tasks_to_list = relationship.get_tasks_to_list(db,list_id=list_id)
    for row in db_tasks_to_list:
        tasks.append(get_single_task(db,task_id=row.task_id))
    return tasks

def move_task(db:Session,list_origin_id:int,task_list_row: schemas_relationship.TaskToListEdit):
    
    return relationship.move_task_to_list(db,list_origin_id==list_origin_id,task_list_row=task_list_row)

def delete_task_everywhere(db:Session,task_id:int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_lists_to_task = relationship.get_lists_to_task(db,task_id=task_id)
    relationship.remove_task_from_lists(db,rows=db_lists_to_task)
    db.delete(db_task)
    db.commit()
    return "horray?"

def remove_task_from_list(db:Session,list_id:int,task_id:int):
    return relationship.remove_task_list_row(db,list_id=list_id, task_id=task_id)