from collections.abc import AsyncGenerator # AsyncGenerator is used to type-hint async functions that yield values, such as FastAPI database dependencies.
from sqlalchemy.ext.asyncio import (
    AsyncSession,  # Creates an asynchronous database engine that manages connections to the database.
    async_sessionmaker,  # A factory that creates new AsyncSession objects whenever you need a database session.
    create_async_engine, # The async database session used to execute queries, inserts, updates, and transactions with await.
)
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # keeps loaded ORM attributes accessible after committing
)

# provides a session to an API request and closes it afterward
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session