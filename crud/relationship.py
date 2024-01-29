from sqlalchemy.orm import Session
from ..db import models
from ..schemas.relationship import ListToUser, TaskToList
from ..schemas import relationship as schemas

def add_task_list_row(db:Session,task_id:int,list_id:int):
    db_task_to_list = models.TaskToList(task_id=task_id,list_id=list_id)
    db.add(db_task_to_list)
    db.commit()
    db.refresh(db_task_to_list)
    return db_task_to_list

def add_user_list_row(db:Session,list_id:int,user_id:int):
    db_row = models.ListToUser(user_id=user_id,list_id=list_id)
    db.add(db_row)
    db.commit()
    db.refresh(db_row)
    return db_row

def get_tasks_to_list(db:Session,list_id:int):
    return db.query(models.TaskToList).filter(models.TaskToList.list_id == list_id).all()\
    
def get_lists_to_task(db:Session,task_id:int):
    return db.query(models.TaskToList).filter(models.TaskToList.task_id == task_id).all()

def get_lists_to_user(db:Session,user_id:int):
    return db.query(models.ListToUser).filter(models.ListToUser.user_id == user_id).all()

def get_users_to_list(db:Session,list_id):
    return db.query(models.ListToUser).filter(models.ListToUser.list_id == list_id).all()

def count_lists_for_task(db:Session,task_id):
    db_rows = db.query(models.TaskToList).filter(models.TaskToList.task_id == task_id).all()
    return len(db_rows)

def move_task_to_list(db:Session,list_origin_id:int,task_list_row: schemas.TaskToListEdit):
    db_task_list = db.query(models.TaskToList).filter(models.TaskToList.list_id == list_origin_id, models.TaskToList.task_id == task_list_row.task_id).first()
    db_task_list.list_id = task_list_row.list_id

    db.add(db_task_list)
    db.commit()
    db.refresh(db_task_list)
    return db_task_list

def remove_task_list_row(db:Session,task_id:int,list_id:int):
    row = db.query(models.TaskToList).filter(models.TaskToList.task_id == task_id, models.TaskToList.list_id == list_id).first()

    db.delete(row)
    db.commit()
    return "success"

def count_users_for_list(db:Session,list_id:int):
    db_rows = db.query(models.ListToUser).filter(models.ListToUser.list_id == list_id).all()

    return len(db_rows)

def remove_task_from_lists(db:Session,rows:list[TaskToList]):
    for row in rows:
        db.delete(row)
    db.commit()

def remove_list_from_users(db:Session,rows:list[ListToUser]):
    for row in rows:
        db.delete(row)
    db.commit()

def remove_list_user_row(db:Session,list_id:int,user_id:int):
    row = db.query(models.ListToUser).filter(models.ListToUser.list_id == list_id, models.ListToUser.user_id == user_id).first()

    db.delete(row)
    db.commit()
    return "success"
