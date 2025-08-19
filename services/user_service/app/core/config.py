from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://crm_user:crm_password@localhost:5432/crm_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    app_name: str = "CRM User Service"
    environment: str = "development"
    debug: bool = True
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()