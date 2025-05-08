import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from api.app.models import models
from api.app.security import get_password_hash
import uuid
from api.app.database_app import get_db
from api.app.main import app
from sqlalchemy import create_engine
from urllib.parse import urlencode

# Banco de dados de teste em memória ou arquivo temporário
TEST_DATABASE_URL = "sqlite:///./test.db"  # Ou "sqlite:///:memory:" para memória

# Criação do engine e sessão
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de testes
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    global os
    if engine.url.database != ":memory:":
        import os

    models.Base.metadata.create_all(bind=engine)
    yield

    # Fechar todas as conexões ativas
    engine.dispose()

    # Remover arquivo SQLite se não for em memória
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

@pytest.fixture
def create_test_user(db: Session):
    def _create_user(
        first_name="Test",
        last_name="User",
        email=None,
        password="123456",
        user_type="patient",
        access_code=None,
    ):
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

            # Criar access code se não existir
            existing_code = db.query(models.AccessCode).filter_by(code=access_code).first()
            if not existing_code:
                new_code = models.AccessCode(code=access_code, email=email, used=False)
                db.add(new_code)
                db.commit()

            professional = models.Professional(
                id=user.id,
                access_code=access_code
            )
            db.add(professional)
            db.commit()
            db.refresh(professional)
        return user
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