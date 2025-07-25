import httpx
from sqlalchemy.orm import Session
import datetime

from .. import crud, models

# --- Ações do Playbook ---

class WebhookAction:
    def __init__(self, config: dict):
        self.url = config.get("url")

    async def execute(self, vulnerability: models.Vulnerability):
        if not self.url:
            raise ValueError("Webhook URL not configured for this action.")

        payload = {
            "vulnerability_id": vulnerability.id,
            "name": vulnerability.name,
            "severity": vulnerability.severity,
            "cvss_score": vulnerability.cvss_score,
            "host": vulnerability.host,
            "description": vulnerability.description,
        }

        async with httpx.AsyncClient() as client:
            print(f"Sending webhook to {self.url} for vuln ID {vulnerability.id}")
            response = await client.post(self.url, json=payload)
            response.raise_for_status() # Lança exceção se o status não for 2xx

# Mapeamento de tipos de ação para classes
ACTION_MAP = {
    "webhook": WebhookAction,
}

# --- Motor de Execução ---

async def execute_playbook(db: Session, playbook_id: int, vulnerability_id: int):
    # 1. Obter os modelos do DB
    playbook = db.query(models.Playbook).filter(models.Playbook.id == playbook_id).first()
    vulnerability = db.query(models.Vulnerability).filter(models.Vulnerability.id == vulnerability_id).first()

    if not playbook or not vulnerability:
        raise ValueError("Playbook or Vulnerability not found.")

    # 2. Registrar a execução
    execution = models.PlaybookExecution(
        playbook_id=playbook_id,
        vulnerability_id=vulnerability_id,
        status="running"
    )
    db.add(execution)
    db.commit()

    try:
        # 3. Executar os passos em ordem
        sorted_steps = sorted(playbook.steps, key=lambda s: s.step_number)
        for step in sorted_steps:
            ActionClass = ACTION_MAP.get(step.action_type)
            if not ActionClass:
                raise NotImplementedError(f"Action type '{step.action_type}' is not implemented.")

            action = ActionClass(config=step.action_config.config)
            await action.execute(vulnerability)

        # 4. Marcar como concluído
        execution.status = "completed"

    except Exception as e:
        print(f"Playbook execution failed: {e}")
        execution.status = "failed"
        raise

    finally:
        execution.completed_at = datetime.datetime.utcnow()
        db.commit()
