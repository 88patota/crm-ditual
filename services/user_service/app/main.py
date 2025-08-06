from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.services.messaging import initialize_messaging, close_messaging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_messaging()
    yield
    # Shutdown
    await close_messaging()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0",
        description="Microserviço de gerenciamento de usuários do CRM",
        lifespan=lifespan
    )
    
    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure adequadamente em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    
    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "CRM User Service is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user_service"}