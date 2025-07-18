from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .... import crud, models, schemas
from ....api import deps
from ....services.gvm_service import GVMService

router = APIRouter()

@router.post("/", response_model=schemas.Scan)
def create_scan(
    *,
    db: Session = Depends(deps.get_db),
    scan_in: schemas.ScanCreate,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Create new scan. (Analyst or Admin)
    """
    config = crud.scanner_config.get_config(db, config_id=scan_in.config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Scanner configuration not found")

    # 1. Registrar o scan no nosso DB
    scan = crud.scan.create_scan(db=db, obj_in=scan_in, user=current_user)

    try:
        # 2. Conectar e iniciar o scan no GVM
        gvm_service = GVMService(config)
        with gvm_service.connect() as gmp:
            target_id = gvm_service.find_or_create_target(gmp, host=scan_in.target_host)
            task_name = f"Scan for {scan_in.target_host} (GCV Scan ID: {scan.id})"
            task_id = gvm_service.create_scan_task(gmp, name=task_name, target_id=target_id)

        # 3. Atualizar nosso DB com o ID da tarefa do GVM e o status
        scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=task_id)
        return scan

    except Exception as e:
        # Se algo der errado com o GVM, marcamos nosso scan como falho
        crud.scan.update_scan_status(db, scan_id=scan.id, status="Failed")
        raise HTTPException(status_code=500, detail=f"Failed to start scan in GVM: {e}")


@router.get("/", response_model=List[schemas.Scan])
def read_scans(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Retrieve scans.
    """
    scans = crud.scan.get_all_scans(db, skip=skip, limit=limit)
    return scans

@router.get("/{scan_id}", response_model=schemas.Scan)
def read_scan(
    *,
    db: Session = Depends(deps.get_db),
    scan_id: int,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Get scan by ID.
    """
    scan = crud.scan.get_scan(db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.post("/{scan_id}/import", response_model=schemas.Msg)
def import_scan_results(
    *,
    db: Session = Depends(deps.get_db),
    scan_id: int,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Import results for a completed scan.
    """
    scan = crud.scan.get_scan(db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not scan.gvm_task_id:
        raise HTTPException(status_code=400, detail="Scan has no GVM task ID.")

    config = scan.config
    gvm_service = GVMService(config)

    try:
        with gvm_service.connect() as gmp:
            # Aqui estamos assumindo que o scan terminou. Uma implementação mais robusta
            # verificaria o status da tarefa no GVM antes de tentar importar.
            vulnerabilities = gvm_service.get_scan_report(gmp, task_id=scan.gvm_task_id)

        crud.vulnerability.bulk_create_vulnerabilities(
            db, scan_id=scan.id, vulnerabilities_data=vulnerabilities
        )

        crud.scan.update_scan_status(db, scan_id=scan.id, status="Done")

        return {"msg": f"Successfully imported {len(vulnerabilities)} vulnerabilities."}

    except Exception as e:
        crud.scan.update_scan_status(db, scan_id=scan.id, status="Import Failed")
        raise HTTPException(status_code=500, detail=f"Failed to import scan results: {e}")
