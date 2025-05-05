import pytest
from fastapi.testclient import TestClient
from api.app.main import app
from sqlalchemy.orm import Session
from api.app.models import models
from api.app.security import get_password_hash
from api.app.database_app import SessionLocal, engine, Base



@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def pytest_addoption(parser):
    """ Adiciona a opção --db-reset ao pytest """
    parser.addoption("--db-reset", action="store_true", default=False, help="Reseta o banco antes dos testes")

@pytest.fixture(scope="function")
def db_reset(request):
    """
       Limpa e recria todas as tabelas do banco de dados antes de cada teste,
       apenas se a flag --db-reset for usada.
       """
    if request.config.getoption("--db-reset"):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine) # remove os dados após o teste
    else:
        yield  # Não faz nada se a flag não for passada

@pytest.fixture
def create_test_user(db: Session):
    def _create_user(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="123456",
        user_type="patient",
        access_code=None,
    ):
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
        response = client.post("/auth/login", json={
            "email": email, "password": senha
        }
       )
        assert response.status_code == 200, f"Erro no login: {response.text}"
        return response.json()["access_token"]
    return _login

@pytest.fixture
def login_test_user(get_auth_token):
    return get_auth_token