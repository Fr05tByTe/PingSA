from __future__ import annotations

from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("pingsa", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.timezone = "Africa/Johannesburg"
celery_app.conf.task_acks_late = True
celery_app.conf.task_default_retry_delay = 30
celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "default"}}
