from fastapi import APIRouter

router = APIRouter(prefix="/property", tags=["property"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "property-ok"}
