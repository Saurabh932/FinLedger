from fastapi import APIRouter
from app.models.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="Healthy!",
        application="FinLedger",
        version="0.1.0"
    )    