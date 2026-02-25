# PingSA MVP

Production-minded WhatsApp automation platform for South Africa built with FastAPI + PostgreSQL + SQLAlchemy + Celery/Redis.

## Features
- WhatsApp webhook verification and inbound processing with dedup + rate limiting.
- Interactive onboarding/main menu payload builders.
- Modular services: Vehicle reminders, Fine monitoring (mock provider), Property search/leads, Safety timers.
- Consent flow, pause/resume, stop fines, delete-data trigger scaffolding.
- AES-GCM + SHA-256 utilities for SA ID handling.
- Structured JSON logs, Prometheus metrics, health/readiness endpoints.
- Celery worker + beat schedules.
- API-key protected admin endpoints.

## Local development
1. Copy env:
   ```bash
   cp .env.example .env
   ```
2. Start stack:
   ```bash
   docker compose up --build
   ```
3. Run migrations:
   ```bash
   docker compose exec api alembic upgrade head
   ```
4. Seed sample data:
   ```bash
   docker compose exec api python scripts/seed.py
   ```

## Simulate WhatsApp webhook
```bash
curl -X POST http://localhost:8000/webhook/whatsapp \
  -H 'Content-Type: application/json' \
  -d '{"entry":[{"changes":[{"value":{"contacts":[{"wa_id":"27820000000"}],"messages":[{"id":"wamid.1","from":"27820000000","text":{"body":"Hi"}}]}}]}]}'
```

## Tests & quality
```bash
pip install -e .[dev]
ruff check .
black --check .
mypy app
pytest -q
```

## Deployment notes (Render/Railway/Fly.io)
- Services: `api` (FastAPI), `worker` (Celery worker), `beat` (Celery beat).
- Add managed PostgreSQL + Redis.
- Required env vars: `DATABASE_URL`, `REDIS_URL`, `WHATSAPP_*`, `ADMIN_API_KEY`, `DATA_ENCRYPTION_KEY`.
- Set web concurrency (`WEB_CONCURRENCY`) and tune Celery worker concurrency.
- Keep health checks on `/health/live` and `/health/ready`.
- Ensure JSON logs are streamed to platform logging.

## Production TODOs
- Approved WhatsApp template registry + template send path.
- Strong auth/RBAC for admin APIs.
- Dead-letter queues and advanced retry policies.
- Full deletion workflow orchestration and audits.
