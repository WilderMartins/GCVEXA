from app.crud.base import CRUDBase
from app.models.collector import Collector
from app.schemas.collector import CollectorCreate, Collector as CollectorSchema

class CRUDCollector(CRUDBase[Collector, CollectorCreate, CollectorSchema]):
    pass

collector = CRUDCollector(Collector)
