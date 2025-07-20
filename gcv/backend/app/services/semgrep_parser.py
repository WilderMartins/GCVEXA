import json

def parse_semgrep_results(file_path: str) -> list:
    """
    Parseia o arquivo de resultados JSON do Semgrep.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

    except FileNotFoundError:
        print(f"Arquivo de resultados não encontrado em: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o JSON do arquivo: {file_path}")

        return []

    vulnerabilities = []
    for result in data.get("results", []):

        check = result.get("check_id", "N/A")

        path = result.get("path", "N/A")
        line = result.get("start", {}).get("line", "N/A")

        vuln_data = {

            "name": f"{check} in {path}",
            "severity": map_severity(result.get("extra", {}).get("severity", "INFO")),
            "cvss_score": 0.0, # Semgrep não fornece CVSS
            "description": result.get("extra", {}).get("message", "No description provided."),
            "host": path, # Usamos o campo 'host' para o caminho do arquivo
            "port": str(line), # Usamos o campo 'port' para a linha

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
