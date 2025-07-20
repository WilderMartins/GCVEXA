def parse_zap_alerts(alerts: list) -> list:
    """
    Parseia a lista de alertas do ZAP para o nosso formato de vulnerabilidade.
    """
    vulnerabilities = []
    for alert in alerts:
        vuln_data = {
            "name": alert.get('name'),
            "severity": map_severity(alert.get('risk')),

            "cvss_score": 0.0, # ZAP não fornece CVSS diretamente, podemos mapear ou calcular
            "description": f"{alert.get('description')}\n\nSolution: {alert.get('solution')}",
            "host": alert.get('url'),
            "port": "", # O ZAP foca em URLs, não em portas específicas

        }
        vulnerabilities.append(vuln_data)
    return vulnerabilities

def map_severity(zap_risk: str) -> str:
    """
    Mapeia o 'risk' do ZAP para a nossa 'severity'.
    """
    mapping = {
        "High": "High",
        "Medium": "Medium",
        "Low": "Low",

        "Informational": "Low" # ou "Info" se quisermos um novo status

    }
    return mapping.get(zap_risk, "Unknown")
