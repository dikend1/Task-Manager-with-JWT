from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from app.db.session import SessionLocal
from app.services import auth_service
from app.schemas.user_schema import UserCreate,UserRead


router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register",response_model=UserRead)
def register(user:UserCreate,db:Session=Depends(get_db)):
    return auth_service.register_user(user,db)

@router.post("/login")
def login(username:str, password:str, db:Session=Depends(get_db)):
    return auth_service.login_user(username,password,db)

