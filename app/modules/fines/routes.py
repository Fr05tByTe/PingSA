from fastapi import APIRouter

router = APIRouter(prefix="/fines", tags=["fines"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "fines-ok"}
