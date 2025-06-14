import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.app.main import app
from api.app.database_app import get_db
from api.app.models import models
from api.app.models.models import Base
from api.app.security import get_password_hash

# Banco de dados de teste em memória ou arquivo temporário
TEST_DATABASE_URL = "sqlite:///./test.db"  # Ou "sqlite:///:memory:" para memória

# Criação do engine e sessão
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de testes
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    if engine.url.database != ":memory:":
        db_path = engine.url.database
        if os.path.exists(db_path):
            os.remove(db_path)

# Dependência override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db  # type: ignore[attr-defined]
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear() # type: ignore[attr-defined]

@pytest.fixture
def create_test_user():
    def _create_user(
        first_name="Test",
        last_name="User",
        email=None,
        password="123456",
        user_type="patient",
        access_code=None,
    ):
        db = TestingSessionLocal()
        try:
            if not email:
                email = f"{uuid.uuid4()}@example.com"

            hashed_password = get_password_hash(password)
            user = models.User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                user_type=user_type,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            if user_type == "professional":
                if not access_code:
                    raise ValueError("Access code is required for professional users")
                existing_code = db.query(models.AccessCode).filter_by(code=access_code).first()
                if not existing_code:
                    db.add(models.AccessCode(code=access_code, email=email, used=False))
                    db.commit()
                professional = models.Professional(id=user.id, access_code=access_code)
                db.add(professional)

            elif user_type == "patient":
                patient = models.Patient(id=user.id)
                db.add(patient)

            db.commit()
            return user.id
        finally:
            db.close()
    return _create_user

@pytest.fixture
def get_auth_token(client):
    def _login(email, senha):
        data = {
            "email": email,
            "password": senha
        }
        response = client.post(
            "/auth/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200, f"Erro no login: {response.text}"
        return response.json()["access_token"]
    return _login

@pytest.fixture
def login_test_user(get_auth_token):
    return get_auth_token

@pytest.fixture
def insert_access_code():
    def _insert(code):
        db = TestingSessionLocal()
        db.add(models.AccessCode(code=code, used=False))
        db.commit()
        db.close()
    return _insert

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("FROM_EMAIL", "test@example.com")
    monkeypatch.setenv("SMTP_USER", "test@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "fakepassword")
    monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")