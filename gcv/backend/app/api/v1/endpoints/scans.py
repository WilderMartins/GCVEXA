from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from ....services import pdf_service, email_service, zap_parser, semgrep_parser, sonarqube_parser
from .... import crud, models, schemas
from ....api import deps
from ....services.gvm_service import GVMService
from ....services.zap_service import ZAPService
from ....services.semgrep_service import SemgrepService
from ....services.sonarqube_service import SonarQubeService

router = APIRouter()

@router.post("/", response_model=schemas.Scan)
async def create_scan(
    *,
    db: Session = Depends(deps.get_db),
    scan_in: schemas.ScanCreate,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Create new scan for a specific asset.

    """
    config = crud.scanner_config.get_config(db, config_id=scan_in.config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Scanner configuration not found")

    asset = crud.asset.get_asset(db, asset_id=scan_in.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id and not any(role.name == "Admin" for role in current_user.roles):
         raise HTTPException(status_code=403, detail="Not enough permissions to scan this asset")

    scan = crud.scan.create_scan(db=db, obj_in=scan_in, user=current_user)
    target_address = asset.address

    try:
        if config.type == "openvas":
            gvm_service = GVMService(config)
            with gvm_service.connect() as gmp:
                target_id = gvm_service.find_or_create_target(gmp, host=target_address)
                task_name = f"Scan for {target_address} (GCV Scan ID: {scan.id})"
                task_id = gvm_service.create_scan_task(gmp, name=task_name, target_id=target_id)
            scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=task_id)

        elif config.type == "zap":
            zap_service = ZAPService(config)
            task_id = zap_service.start_scan(target_url=target_address)

            scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=task_id)

        elif config.type == "semgrep":
            semgrep_service = SemgrepService()
            try:
                results_path = semgrep_service.run_scan(repo_url=target_address)
                vulnerabilities = semgrep_parser.parse_semgrep_results(results_path)
                crud.vulnerability.bulk_create_vulnerabilities(db, scan_id=scan.id, vulnerabilities_data=vulnerabilities)

                scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Done")
                await email_service.send_scan_completion_email(scan)
            finally:
                semgrep_service.cleanup()

        elif config.type == "sonarqube":
            project_key = target_address.split("/")[-1].replace(".git", "") + f"_{scan.id}"
            sonarqube_service = SonarQubeService(config)
            sonarqube_service.provision_project_and_run_scan(project_key=project_key, repo_url=target_address)

            scan = crud.scan.update_scan_status(db, scan_id=scan.id, status="Running", gvm_task_id=project_key)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scanner type: {config.type}")

        return scan

    except Exception as e:
        crud.scan.update_scan_status(db, scan_id=scan.id, status="Failed")
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")

# O resto dos endpoints (read_scans, import_scan_results, etc.) permanece aqui...

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
            if zap_service.get_scan_status(scan.gvm_task_id) < 100:
                 raise HTTPException(status_code=400, detail="ZAP scan is still running.")
            alerts = zap_service.get_scan_results(target_url=scan.asset.address)
            vulnerabilities = zap_parser.parse_zap_alerts(alerts)

        elif config.type == "sonarqube":
            sonarqube_service = SonarQubeService(config)

            issues = sonarqube_service.get_scan_results(project_key=scan.gvm_task_id)
            vulnerabilities = sonarqube_parser.parse_sonarqube_issues(issues)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scanner type for import: {config.type}")

        crud.vulnerability.process_vulnerabilities_from_scan(
            db, scan=scan, vulnerabilities_data=vulnerabilities

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
