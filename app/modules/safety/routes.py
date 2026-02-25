from fastapi import APIRouter

router = APIRouter(prefix="/safety", tags=["safety"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "safety-ok"}
