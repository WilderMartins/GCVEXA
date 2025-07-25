from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Collector)
def create_collector(
    *,
    db: Session = Depends(deps.get_db),
    collector_in: schemas.CollectorCreate,
) -> schemas.Collector:
    """
    Create new collector.
    """
    collector = crud.collector.create(db=db, obj_in=collector_in)
    return collector

@router.get("/", response_model=List[schemas.Collector])
def read_collectors(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.Collector]:
    """
    Retrieve collectors.
    """
    collectors = crud.collector.get_multi(db, skip=skip, limit=limit)
    return collectors
