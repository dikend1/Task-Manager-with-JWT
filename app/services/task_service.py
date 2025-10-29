from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app import models,schemas

def create_task(db:Session,task_data: schemas.task_schema.TaskCreate,user_id:int):
    new_task = models.Task(**task_data.dict(),owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db:Session,user_id:int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_task_by_id(db:Session, user_id:int,task_id:int):
    task = db.query(models.Task).filter(models.Task.id == task_id,models.Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    return task

def update_task(db:Session, task_id:int,task_update:schemas.TaskCreate,user_id:int):
    task = get_task_by_id(db, task_id, user_id)
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task,key,value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db:Session, task_id:int, user_id:int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


