from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

from .. import crud, schemas

# Helper para criar um usuário admin e obter um token
def get_admin_token_headers(client: TestClient, db: Session) -> dict:
    client.post(f"/api/v1/users/", json={"email": "admin_scan@test.com", "password": "pw", "full_name": "Admin Scan"})
    login_data = {"username": "admin_scan@test.com", "password": "pw"}
    r = client.post(f"/api/v1/login/access-token", data=login_data)
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_openvas_scan(client: TestClient, db: Session):
    # Setup: Criar uma config de scanner
    headers = get_admin_token_headers(client, db)
    client.post("/api/v1/scanners/configs/", headers=headers, json={
        "name": "Test OpenVAS", "url": "tls://localhost", "username": "u", "password": "p", "type": "openvas"
    })

    # Mockar o GVMService
    with patch("app.api.v1.endpoints.scans.GVMService") as mock_gvm:
        # Configurar o mock para retornar um ID de tarefa falso
        mock_instance = MagicMock()
        mock_instance.connect.return_value.__enter__.return_value = MagicMock()
        mock_instance.create_scan_task.return_value = "fake-gvm-task-id"
        mock_gvm.return_value = mock_instance

        # Ação: Chamar o endpoint de criação de scan
        scan_data = {"target_host": "127.0.0.1", "config_id": 1}
        response = client.post("/api/v1/scans/", headers=headers, json=scan_data)

        # Asserções
        assert response.status_code == 200
        data = response.json()
        assert data["target_host"] == "127.0.0.1"
        assert data["status"] == "Running"
        assert data["gvm_task_id"] == "fake-gvm-task-id"
        mock_gvm.assert_called_once() # Verificar se o serviço foi chamado

def test_import_openvas_results(client: TestClient, db: Session):
    headers = get_admin_token_headers(client, db)
    client.post("/api/v1/scanners/configs/", headers=headers, json={
        "name": "Test OpenVAS Import", "url": "tls://localhost", "username": "u", "password": "p", "type": "openvas"
    })
    # Criar um scan para poder importar
    scan_resp = client.post("/api/v1/scans/", headers=headers, json={"target_host": "1.1.1.1", "config_id": 1})
    scan_id = scan_resp.json()["id"]

    # Mockar o GVMService e o email_service
    with patch("app.api.v1.endpoints.scans.GVMService") as mock_gvm, \
         patch("app.api.v1.endpoints.scans.email_service.send_scan_completion_email") as mock_email:

        mock_gvm_instance = MagicMock()
        # Simular o retorno de uma vulnerabilidade
        mock_gvm_instance.get_scan_report.return_value = [{
            "name": "Fake Vuln", "severity": "High", "cvss_score": 9.0,
            "description": "desc", "host": "1.1.1.1", "port": "443"
        }]
        mock_gvm.return_value = mock_gvm_instance

        # Ação: Chamar o endpoint de importação
        response = client.post(f"/api/v1/scans/{scan_id}/import", headers=headers)

        # Asserções
        assert response.status_code == 200
        assert "Successfully imported 1 vulnerabilities" in response.json()["msg"]

        # Verificar se a vulnerabilidade foi salva no DB
        scan = crud.scan.get_scan(db, scan_id)
        assert scan.status == "Done"
        assert len(scan.vulnerabilities) == 1
        assert scan.vulnerabilities[0].name == "Fake Vuln"

        # Verificar se o e-mail foi chamado
        mock_email.assert_called_once()
