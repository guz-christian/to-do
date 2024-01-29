
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import list as schemas
from . import relationship

def share_list(db:Session,user_id:int,list_id):
    return relationship.add_user_list_row(db,user_id=user_id,list_id=list_id)

def create_list(db:Session,list: schemas.ListCreate,user_id:int):
    db_list = models.List(**list.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)

    # add_list_user_relation(db,user_id=user_id,list_id=db_list.id)
    relationship.add_user_list_row(db,user_id=user_id,list_id=db_list.id)
    return db_list

def edit_list(db:Session, list_id:int, list_edits: schemas.ListCreate):
    db_list = get_list(db,list_id=list_id)
    db_list.name = list_edits.name
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def get_list(db:Session,list_id:int):
    db_list = db.query(models.List).filter(models.List.id == list_id).first()
    return db_list

def get_user_lists(db:Session,user_id:int):
    lists = []
    db_list_to_user = relationship.get_lists_to_user(db,user_id=user_id)
    for row in db_list_to_user:
        lists.append(db.query(models.List).filter(models.List.id == row.list_id).first())
    return lists

def delete_list_everywhere(db:Session,list_id):
    db_relationship_rows = relationship.get_users_to_list(db,list_id=list_id)
    relationship.remove_list_from_users(db,rows=db_relationship_rows)
    db_list = get_list(db,list_id=list_id)
    db.delete(db_list)
    db.commit()

    return "removed from all users"

def remove_list_from_user(db:Session, list_id: int, user_id:int):
    relationship.remove_list_user_row(db,list_id=list_id,user_id=user_id)
    return "removed!"
