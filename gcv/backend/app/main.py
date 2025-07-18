from fastapi import FastAPI
from .db.session import engine
from .db.base_class import Base
from .api.v1.endpoints import login

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="GCV - Sistema de Gestão de Vulnerabilidades")

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(login.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao GCV API"}
