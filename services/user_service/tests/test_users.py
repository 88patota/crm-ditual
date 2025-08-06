import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.user import UserRole


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
async def setup_database():
    """Setup test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def test_create_user(setup_database):
    """Test criar usuário"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123",
        "role": UserRole.VENDAS.value
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == user_data["role"]
    assert "id" in data


def test_create_user_duplicate_email(setup_database):
    """Test criar usuário com email duplicado"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "full_name": "User One",
        "password": "password123",
        "role": UserRole.VENDAS.value
    }
    
    # Primeiro usuário
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    # Segundo usuário com mesmo email
    user_data["username"] = "user2"
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "Email já está em uso" in response.json()["detail"]


def test_login_user(setup_database):
    """Test login de usuário"""
    # Criar usuário primeiro
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "full_name": "Login User",
        "password": "loginpassword123",
        "role": UserRole.ADMIN.value
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    # Fazer login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword123"
    }
    
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(setup_database):
    """Test login com credenciais inválidas"""
    login_data = {
        "username": "invaliduser",
        "password": "invalidpassword"
    }
    
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"]


def test_get_users(setup_database):
    """Test listar usuários"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "CRM User Service is running!" in response.json()["message"]