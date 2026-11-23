from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health import HealthResponse
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="Healthy!",
        application="FinLedger",
        version="0.1.0"
    )

@router.get("/ready", tags=["Health"])
async def readiness_check(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Databse is unavailable"
        ) from exc

    return {
        "status":"ready",
        "database":"connected"
    }