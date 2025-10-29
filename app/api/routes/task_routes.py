from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import task_service,auth_service
from app.core.security import decode_access_token
from app.schemas.task_schema import TaskCreate,TaskRead,TaskUpdate
from app import models



security = HTTPBearer()
router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db:Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.post("/",response_model=TaskRead)
def create_task(task:TaskCreate, db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    return task_service.create_task(db,task,current_user.id)

@router.get("/",response_model=list[TaskRead])
def get_user_tasks(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return task_service.get_tasks(db,current_user.id)

@router.get("/{task_id}",response_model=TaskRead)
def get_task_by_id(task_id:int,db: Session = Depends(get_db),  current_user=Depends(get_current_user)):
    task = task_service.get_task_by_id(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    return task

@router.put("/{task_id}",response_model=TaskRead)
def update_task(task_id: int,task:TaskUpdate,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    updated = task_service.update_task(db,task_id,task,current_user.id)
    if not updated:
        raise HTTPException(status_code=404,detail="Task not found or not yours")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int,db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    deleted = task_service.delete_task(db,task_id,current_user.id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Task not found or not yours")
    return {"detail": "Task deleted successfully"}


@router.get("/search/",response_model=list[TaskRead])
def search_tasks(q:str, db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    tasks = task_service.search_tasks(db,current_user.id,q)
    return tasks