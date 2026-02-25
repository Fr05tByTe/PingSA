from __future__ import annotations

from celery.schedules import crontab

beat_schedule = {
    "daily_license_expiry_job": {"task": "app.workers.tasks.daily_license_expiry_job", "schedule": crontab(minute=0, hour=8)},
    "fines_monitoring_job": {"task": "app.workers.tasks.fines_monitoring_job", "schedule": crontab(minute=0, hour="*/48")},
    "safety_tick_job": {"task": "app.workers.tasks.safety_tick_job", "schedule": 60.0},
    "cleanup_job": {"task": "app.workers.tasks.cleanup_job", "schedule": crontab(minute=0, hour=2)},
}
