import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import budgets, dashboard
from app.core.database import create_tables

app = FastAPI(
    title="Budget Service API",
    description="Serviço de orçamentos e cálculos de rentabilidade - CRM Ditual",
    version="1.0.0",
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Usar domínios específicos em produção
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["budgets"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Budget Service API - CRM Ditual"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "budget_service"}