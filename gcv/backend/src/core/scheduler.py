from apscheduler.schedulers.background import BackgroundScheduler
from app import crud
from app.db.session import SessionLocal
from app.collectors import file_collector

scheduler = BackgroundScheduler()

def run_collectors():
    """
    Run all configured collectors.
    """
    db = SessionLocal()
    collectors = crud.collector.get_multi(db)
    for collector in collectors:
        if collector.collector_type == "file":
            file_collector.run(collector.config)
    db.close()

def start_scheduler():
    """
    Start the scheduler.
    """
    scheduler.add_job(run_collectors, "interval", minutes=60)
    scheduler.start()

def shutdown_scheduler():
    """
    Shutdown the scheduler.
    """
    scheduler.shutdown()
