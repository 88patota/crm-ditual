import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "USER_SERVICE_DATABASE_URL", 
        "postgresql+asyncpg://crm_user:crm_password@localhost:5432/crm_db"
    )
    
    # Redis
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    
    @property
    def redis_url(self) -> str:
        """Construir URL do Redis"""
        if self.redis_password:
            # URL encode the password to handle special characters
            from urllib.parse import quote_plus
            encoded_password = quote_plus(self.redis_password)
            return f"redis://:{encoded_password}@{self.redis_host}:{self.redis_port}"
        return f"redis://{self.redis_host}:{self.redis_port}"
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application
    app_name: str = os.getenv("APP_NAME", "CRM User Service")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # API
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    
    class Config:
        env_file = ".env"


settings = Settings()