from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import UserRegsiter, UserResponse
from app.services.auth import AuthService, DuplicateEmailError

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
async def register_user(user_data: UserRegsiter, session: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    try:
        user = await AuthService.register_user(session, user_data)
        return UserResponse.model_validate(user)

    except DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc