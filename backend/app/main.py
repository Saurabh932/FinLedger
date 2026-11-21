from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, logger

settings = get_settings()
configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await logger.ainfo(
        "application_started",
        application=settings.APP_NAME,
        environment=settings.ENVIRONMENT
    )

    yield
    
    await logger.ainfo("application_stopped")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["GET","POST","PUT","PATCH","DELETE"],
        allow_headers=["Authorization", "Content-Type"]
    )

    app.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX,
    )

    return app

app = create_app()