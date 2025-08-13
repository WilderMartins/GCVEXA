from fastapi import FastAPI
from .db.session import engine, SessionLocal
from .db.base_class import Base
from .api.v1.endpoints import login, scanner_configs, scans, dashboard, mfa, customization, vulnerability_definitions, setup, playbooks, reporting, assets, collectors
from . import crud
from .core.scheduler import start_scheduler, shutdown_scheduler

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
    start_scheduler()

@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()

app.include_router(login.router, prefix="/api/v1", tags=["Login"])
app.include_router(scanner_configs.router, prefix="/api/v1/scanners/configs", tags=["Scanner Configurations"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["Scans"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(mfa.router, prefix="/api/v1/mfa", tags=["MFA"])
app.include_router(customization.router, prefix="/api/v1/customization", tags=["Customization"])
app.include_router(vulnerability_definitions.router, prefix="/api/v1/vulnerabilities", tags=["Vulnerabilities"])
app.include_router(setup.router, prefix="/api/v1/setup", tags=["Setup"])
app.include_router(playbooks.router, prefix="/api/v1/playbooks", tags=["Playbooks"])
app.include_router(reporting.router, prefix="/api/v1/reporting", tags=["Reporting"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(collectors.router, prefix="/api/v1/collectors", tags=["Collectors"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao GCV API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
