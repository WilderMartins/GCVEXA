import json
from app.schemas import ScanCreate, VulnerabilityCreate

def parse(data: str) -> ScanCreate:
    """
    Parse BurpSuite scan results.
    """
    scan_data = json.loads(data)
    vulnerabilities = []
    for issue in scan_data["issue_events"]:
        vulnerability = VulnerabilityCreate(
            name=issue["issue"]["name"],
            description=issue["issue"]["description"],
            severity=issue["issue"]["severity"],
            remediation=issue["issue"]["remediation"],
            status="Aberta",
        )
        vulnerabilities.append(vulnerability)
    scan = ScanCreate(
        name="Escaneamento do BurpSuite",
        asset_id=1,
        vulnerabilities=vulnerabilities,
    )
    return scan
