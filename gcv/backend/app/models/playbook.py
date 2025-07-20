from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class Playbook(Base):
    __tablename__ = "playbooks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    steps = relationship("PlaybookStep", back_populates="playbook", cascade="all, delete-orphan")

class PlaybookStep(Base):
    __tablename__ = "playbook_steps"
    id = Column(Integer, primary_key=True, index=True)
    step_number = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False) # e.g., "webhook", "email", "jira_ticket"

    playbook_id = Column(Integer, ForeignKey("playbooks.id"))
    playbook = relationship("Playbook", back_populates="steps")

    action_config = relationship("PlaybookAction", uselist=False, back_populates="step", cascade="all, delete-orphan")

class PlaybookAction(Base):
    __tablename__ = "playbook_actions"
    id = Column(Integer, primary_key=True, index=True)
    config = Column(JSON, nullable=False) # e.g., {"url": "https://hooks.slack.com/..."}

    step_id = Column(Integer, ForeignKey("playbook_steps.id"))
    step = relationship("PlaybookStep", back_populates="action_config")

class PlaybookExecution(Base):
    __tablename__ = "playbook_executions"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending") # pending, running, completed, failed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    playbook_id = Column(Integer, ForeignKey("playbooks.id"))
    vulnerability_id = Column(Integer, ForeignKey("vulnerability_occurrences.id"))

    playbook = relationship("Playbook")
    vulnerability = relationship("VulnerabilityOccurrence")
