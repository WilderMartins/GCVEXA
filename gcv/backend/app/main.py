from fastapi import FastAPI
from .db.session import engine, SessionLocal
from .db.base_class import Base
from .api.v1.endpoints import login, scanner_configs, scans
from . import crud

def create_initial_data():
    db = SessionLocal()
    crud.role.get_or_create(db, name="Admin", description="Total system control")
    crud.role.get_or_create(db, name="Analyst", description="Can view dashboards, run scans, and generate reports")
    db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="GCV - Sistema de Gestão de Vulnerabilidades")

@app.on_event("startup")
def on_startup():
    create_tables()
    create_initial_data()

app.include_router(login.router, prefix="/api/v1", tags=["Login"])
app.include_router(scanner_configs.router, prefix="/api/v1/scanners/configs", tags=["Scanner Configurations"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["Scans"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao GCV API"}
