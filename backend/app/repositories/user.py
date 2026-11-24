from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository:

    @staticmethod
    async def get_by_email(
        session: AsyncSession,
        email: str,
    ) -> User | None:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    
    @staticmethod
    async def create(
        session: AsyncSession,
        *,
        full_name: str,
        email: str,
        hashed_password: str
    ) -> User:
        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password
        )

        session.add(user) # registers the new object with the session.
        await session.flush() # sends the insert to PostgreSQL without committing the transaction.

        return user