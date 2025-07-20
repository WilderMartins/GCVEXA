def parse_sonarqube_issues(issues: list) -> list:
    """
    Parseia a lista de 'issues' do SonarQube para o nosso formato de vulnerabilidade.
    """
    vulnerabilities = []
    for issue in issues:
        component = issue.get('component', 'N/A')
        line = issue.get('line', 'N/A')

        vuln_data = {
            "name": issue.get('message'),
            "severity": map_severity(issue.get('severity')),
            "cvss_score": 0.0, # SonarQube não fornece CVSS diretamente
            "description": f"Rule: {issue.get('rule')}\nComponent: {component}",
            "host": component, # Usamos o campo 'host' para o componente/arquivo
            "port": str(line), # Usamos o campo 'port' para a linha
        }
        vulnerabilities.append(vuln_data)

    return vulnerabilities

def map_severity(sonar_severity: str) -> str:
    """
    Mapeia a severidade do SonarQube para a nossa.
    """
    mapping = {
        "BLOCKER": "Critical",
        "CRITICAL": "High",
        "MAJOR": "High",
        "MINOR": "Medium",
        "INFO": "Low"
    }
    return mapping.get(sonar_severity, "Unknown")
