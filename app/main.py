from fastapi import FastAPI

app = FastAPI(title="Ruku Palm Service", version="1.0.0")

from app.db.session import init_db
from app.api.v1 import users

app = FastAPI(title="FastAPI + PostgreSQL")

@app.on_event("startup")
def startup_event():
    init_db()  # crea tablas si no existen

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

