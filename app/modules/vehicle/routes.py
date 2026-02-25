from fastapi import APIRouter

router = APIRouter(prefix="/vehicle", tags=["vehicle"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "vehicle-ok"}
