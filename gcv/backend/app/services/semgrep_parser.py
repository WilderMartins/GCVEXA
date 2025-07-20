import json

def parse_semgrep_results(file_path: str) -> list:
    """
    Parseia o arquivo de resultados JSON do Semgrep.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    vulnerabilities = []
    for result in data.get("results", []):
        check_id = result.get("check_id", "N/A")
        path = result.get("path", "N/A")
        line = result.get("start", {}).get("line", "N/A")

        vuln_data = {
            "name": f"{check_id} in {path}",
            "severity": map_severity(result.get("extra", {}).get("severity", "INFO")),
            "description": result.get("extra", {}).get("message", "No description provided."),
            "host": path,
            "port": str(line),
            # Usar o ID da regra como a parte principal da assinatura para correlação
            "signature_id": check_id
        }
        vulnerabilities.append(vuln_data)

    return vulnerabilities

def map_severity(semgrep_severity: str) -> str:
    """
    Mapeia a severidade do Semgrep para a nossa.
    """
    mapping = {
        "ERROR": "High",
        "WARNING": "Medium",
        "INFO": "Low"
    }
    return mapping.get(semgrep_severity, "Unknown")
