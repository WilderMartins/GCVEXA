from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from ....services import pdf_service, email_service, zap_parser

from .... import crud, models, schemas
from ....api import deps
from ....services.gvm_service import GVMService
from ....services.zap_service import ZAPService

router = APIRouter()

@router.post("/", response_model=schemas.Scan)
def create_scan(
    *,
    db: Session = Depends(deps.get_db),
    scan_in: schemas.ScanCreate,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Create new scan, orchestrating based on scanner type. (Analyst or Admin)
    """
    config = crud.scanner_config.get_config(db, config_id=scan_in.config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Scanner configuration not found")

    scan = crud.scan.create_scan(db=db, obj_in=scan_in, user=current_user)

    try:
        if config.type == "openvas":
            gvm_service = GVMService(config)
            with gvm_service.connect() as gmp:
                target_id = gvm_service.find_or_create_target(gmp, host=scan_in.target_host)
                task_name = f"Scan for {scan_in.target_host} (GCV Scan ID: {scan.id})"
                task_id = gvm_service.create_scan_task(gmp, name=task_name, target_id=target_id)
            scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=task_id)

        elif config.type == "zap":
            zap_service = ZAPService(config)
            task_id = zap_service.start_scan(target_url=scan_in.target_host)
            # O ZAP Spider + Active Scan pode demorar, então marcamos como "Running".
            # O ID da tarefa aqui é o ID do Active Scan.
            scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=task_id)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scanner type: {config.type}")

        return scan

    except Exception as e:
        crud.scan.update_scan_status(db, scan_id=scan.id, status="Failed")
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")


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
async def import_scan_results(
    *,
    db: Session = Depends(deps.get_db),
    scan_id: int,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Import results for a completed scan and send notification.
    """
    scan = crud.scan.get_scan(db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    config = scan.config
    vulnerabilities = []

    try:
        if config.type == "openvas":
            if not scan.gvm_task_id:
                raise HTTPException(status_code=400, detail="Scan has no GVM task ID.")
            gvm_service = GVMService(config)
            with gvm_service.connect() as gmp:
                vulnerabilities = gvm_service.get_scan_report(gmp, task_id=scan.gvm_task_id)

        elif config.type == "zap":
            zap_service = ZAPService(config)
            # Para o ZAP, o "task_id" é o ID do Active Scan.
            # Precisamos verificar se o scan está concluído.
            if zap_service.get_scan_status(scan.gvm_task_id) < 100:
                 raise HTTPException(status_code=400, detail="ZAP scan is still running.")
            alerts = zap_service.get_scan_results(target_url=scan.target_host)
            vulnerabilities = zap_parser.parse_zap_alerts(alerts)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scanner type for import: {config.type}")

        crud.vulnerability.bulk_create_vulnerabilities(
            db, scan_id=scan.id, vulnerabilities_data=vulnerabilities
        )

        scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Done")

        await email_service.send_scan_completion_email(scan)

        return {"msg": f"Successfully imported {len(vulnerabilities)} vulnerabilities. Notification sent."}

    except Exception as e:
        crud.scan.update_scan_status(db, scan_id=scan.id, status="Import Failed")
        raise HTTPException(status_code=500, detail=f"Failed to import scan results: {e}")

@router.get("/{scan_id}/report", response_class=StreamingResponse)
def download_scan_report(
    *,
    db: Session = Depends(deps.get_db),
    scan_id: int,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Download a PDF report for a scan.
    """
    scan = crud.scan.get_scan(db, scan_id=scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status != "Done":
        raise HTTPException(status_code=400, detail="Report can only be generated for 'Done' scans.")

    pdf_buffer = pdf_service.create_scan_report(scan)

    headers = {
        'Content-Disposition': f'attachment; filename="gcv_scan_report_{scan.id}.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
