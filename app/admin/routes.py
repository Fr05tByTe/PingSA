from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.models import PropertyAgent, PropertyLead, User

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(x_admin_api_key: str = Header(default="")) -> None:
    if x_admin_api_key != get_settings().admin_api_key:
        raise HTTPException(status_code=401, detail="unauthorized")


@router.get("/users", dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)) -> list[str]:
    return [u.phone for u in db.scalars(select(User)).all()]


@router.get("/leads", dependencies=[Depends(require_admin)])
def leads(db: Session = Depends(get_db)) -> list[int]:
    return [l.id for l in db.scalars(select(PropertyLead)).all()]


@router.post("/agents", dependencies=[Depends(require_admin)])
def create_agent(payload: dict[str, str], db: Session = Depends(get_db)) -> dict[str, int]:
    agent = PropertyAgent(**payload)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return {"id": agent.id}
