from __future__ import annotations

from datetime import date, datetime

from app.core.db import SessionLocal
from app.core.metrics import job_failures_total, job_runs_total
from app.modules.safety.service import tick_expired
from app.modules.vehicle.service import reminders_due
from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, soft_time_limit=30)
def daily_license_expiry_job(self: object) -> int:
    _ = self
    job_runs_total.labels(job="daily_license_expiry_job").inc()
    try:
        db = SessionLocal()
        due = reminders_due(db, date.today())
        return len(due)
    except Exception:
        job_failures_total.labels(job="daily_license_expiry_job").inc()
        raise


@celery_app.task(bind=True, max_retries=3, soft_time_limit=30)
def fines_monitoring_job(self: object) -> int:
    _ = self
    job_runs_total.labels(job="fines_monitoring_job").inc()
    return 0


@celery_app.task(bind=True, max_retries=1, soft_time_limit=20)
def safety_tick_job(self: object) -> int:
    _ = self
    db = SessionLocal()
    job_runs_total.labels(job="safety_tick_job").inc()
    return len(tick_expired(db, datetime.utcnow()))


@celery_app.task(bind=True, max_retries=1, soft_time_limit=20)
def cleanup_job(self: object) -> int:
    _ = self
    job_runs_total.labels(job="cleanup_job").inc()
    return 0
