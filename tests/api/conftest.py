import pytest
from fastapi.testclient import TestClient
from api.app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def create_user(client):
    def _create_user(nome, email, senha, aceitou_termos, user_type="patient"):
        response = client.post("/users/", json={
            "nome": nome,
            "email": email,
            "senha": senha,
            "aceitou_termos": aceitou_termos,
            "user_type": user_type
        })
        return response
    return _create_user