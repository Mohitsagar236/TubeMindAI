from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/providers")
def providers():
    return {"providers": [{"id": "openai", "enabled": True}], "apiKeyStorage": "client"}
