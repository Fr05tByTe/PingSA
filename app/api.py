from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from redis import Redis
from sqlalchemy.orm import Session

from app.admin.routes import router as admin_router
from app.core.config import get_settings
from app.core.db import get_db
from app.core.health import live, ready
from app.core.idempotency import is_duplicate_message
from app.core.metrics import inbound_messages_total, webhook_duplicates_total
from app.core.notification_service import friendly_cooldown
from app.core.rate_limit import check_rate_limit
from app.core.session_manager import route_text
from app.core.user_service import get_or_create_user, update_last_inbound
from app.core.whatsapp_webhook import parse_inbound_messages
from app.modules.fines.routes import router as fines_router
from app.modules.property.routes import router as property_router
from app.modules.safety.routes import router as safety_router
from app.modules.vehicle.routes import router as vehicle_router

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


@router.get("/webhook/whatsapp")
def verify_webhook(
    mode: str = Query(default="", alias="hub.mode"),
    token: str = Query(default="", alias="hub.verify_token"),
    challenge: str = Query(default="", alias="hub.challenge"),
) -> PlainTextResponse:
    if mode == "subscribe" and token == settings.webhook_verify_token:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="forbidden")


@router.post("/webhook/whatsapp")
def inbound_webhook(payload: dict, request: Request, db: Session = Depends(get_db)) -> dict[str, str]:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    for msg in parse_inbound_messages(payload):
        if not msg.message_id:
            continue
        if is_duplicate_message(db, msg.message_id):
            webhook_duplicates_total.inc()
            continue
        user = get_or_create_user(db, msg.phone)
        update_last_inbound(db, user)
        if not check_rate_limit(redis_client, msg.phone, settings.rate_limit_per_minute):
            _ = friendly_cooldown(msg.phone)
            continue
        inbound_messages_total.inc()
        _responses = route_text(msg.phone, msg.text)
    logger.info("processed webhook", extra={"request_id": request_id})
    return {"status": "ok"}


@router.get("/health/live")
def live_endpoint() -> dict[str, str]:
    return live()


@router.get("/health/ready")
def ready_endpoint(db: Session = Depends(get_db)) -> dict[str, str]:
    return ready(db, redis_client)


@router.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


router.include_router(vehicle_router)
router.include_router(fines_router)
router.include_router(property_router)
router.include_router(safety_router)
router.include_router(admin_router)
