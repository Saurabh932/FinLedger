from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserRegsiter


class DuplicateEmailError(Exception):
    pass

class AuthService:

    @staticmethod
    async def register_user(
        session: AsyncSession,
        user_data: UserRegsiter
    ) -> User:
        
        existing_user = await UserRepository.get_by_email(
            session,
            user_data.email,
        )

        if existing_user:
            raise DuplicateEmailError("Email is already registered")

        hashed_password = hash_password(user_data.password)

        try:
            user = await UserRepository.create(
                session,
                full_name=user_data.full_name,
                email=user_data.email,
                hashed_password=hashed_password
            )

            await session.commit()
            await session.refresh(user)

            return user
        
        except IntegrityError as exc:
            await session.rollback()

            # PostgresSQL unique-constraint violation
            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise DuplicateEmailError(
                    "Email is already registered"
                ) from exc

            raise

        except Exception:
            await session.rollback()
            raise