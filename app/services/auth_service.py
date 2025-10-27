from fastapi import HTTPException,status,Depends
from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import models,schemas


def register_user(user_data: schemas.user_schema.UserCreate, db:Session):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed_pw = hash_password(user_data.password)
    new_user = models.User(username = user_data.username,email = user_data.email,password = hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(username: str, password: str, db:Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user or not verify_password(password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    
    token = create_access_token({"sub":user.password})
    return {"access_token": token, "token_type": "bearer"}





