def parse_zap_alerts(alerts: list) -> list:
    """
    Parseia a lista de alertas do ZAP para o nosso formato de vulnerabilidade.
    """
    vulnerabilities = []
    for alert in alerts:
        vuln_data = {
            "name": alert.get('name'),
            "severity": map_severity(alert.get('risk')),
            "description": f"{alert.get('description')}\n\nSolution: {alert.get('solution')}",
            "host": alert.get('url'),
            "port": "",
            # Usar o ID do plugin como a parte principal da assinatura para correlação
            "signature_id": alert.get('pluginId')
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
        "Informational": "Low"
    }
    return mapping.get(zap_risk, "Unknown")
