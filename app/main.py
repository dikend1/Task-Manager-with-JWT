from fastapi import FastAPI
from app.api.routes import auth_routes,task_routes
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Task Manager with JWT")

app.include_router(auth_routes.router)
app.include_router(task_routes.router)