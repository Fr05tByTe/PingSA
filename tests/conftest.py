from __future__ import annotations

import base64

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core import db as db_mod
from app.core.db import Base
from app.main import app


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATA_ENCRYPTION_KEY", base64.b64encode(b"0" * 32).decode())


@pytest.fixture()
def session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, class_=Session)
    with SessionLocal() as s:
        yield s


@pytest.fixture()
def client(session: Session) -> TestClient:
    def _get_db() -> Session:
        yield session

    app.dependency_overrides[db_mod.get_db] = _get_db
    return TestClient(app)
