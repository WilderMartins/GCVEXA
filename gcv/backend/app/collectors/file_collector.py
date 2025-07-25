import os
from app.schemas import ScanCreate
from app.parsers.dispatcher import get_parser
import requests

def run(collector_config: dict):
    """
    Run the file collector.
    """
    parser = get_parser(collector_config["tool"])
    with open(collector_config["path"], "r") as f:
        scan_data = f.read()
    scan_in = parser.parse(scan_data)

    # Enviar para a API
    api_url = "http://localhost:8000/api/v1/scans/import"
    response = requests.post(api_url, params={"tool": collector_config["tool"]}, files={"file": (os.path.basename(collector_config["path"]), scan_data)})
    response.raise_for_status()
