import pytest
import uuid

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())

def test_register_user_success(client, unique_email):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Usuario",
        "email": unique_email,
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 201, f"Esperado status 201, recebido {response.status_code}: {response.text}"
    assert response.json()["email"] == unique_email


def test_successful_login(client, create_test_user, unique_email):
    create_test_user("Login", "User", unique_email, "123456", user_type="patient")
    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "123456"
    })
    assert response.status_code == 200, f"Esperado 200, recebido {response.status_code}: {response.text}"
    assert "access_token" in response.json()


def test_login_wrong_password(client, create_test_user, unique_email):
    create_test_user("Wrong", "Pass", unique_email, "123456", user_type="patient")
    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "wrongpass"
    })
    assert response.status_code == 401, f"Esperado 401, recebido {response.status_code}: {response.text}"
    assert "Credenciais inválidas" in response.json()["detail"]


def test_register_user_with_short_password(client, unique_email):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Curta",
        "email": unique_email,
        "password": "123",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert any("senha" in d.get("msg", "") for d in response.json()["detail"]), "Mensagem de senha curta não encontrada"


def test_register_user_missing_required_field(client, unique_email):
    response = client.post("/users/", json={
        "email": unique_email,
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert any("field required" in d["msg"].lower() for d in response.json()["detail"])


def test_login_nonexistent_email(client):
    response = client.post("/auth/login", json={
        "email": "naoexiste@example.com",
        "password": "123456"
    })
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}. Detalhes: {response.json()}"
    assert "Credenciais inválidas" in response.json()["detail"]


def test_login_with_empty_password(client, create_test_user, unique_email):
    create_test_user("Teste", "Vazio", unique_email, "123456", user_type="patient")
    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": ""
    })
    assert response.status_code == 422, f"Esperado 422, obtido {response.status_code}. Detalhes: {response.text}"
    assert "password" in response.text


def test_access_with_invalid_token(client):
    response = client.get("/appointment/")
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}"
    assert "Not authenticated" in response.json()["detail"]


@pytest.mark.parametrize("invalid_email", [
    "teste@", "semarroba.com", "@invalido.com", "inválido@@email.com", "user@.com"
])
def test_register_with_invalid_emails(client, invalid_email):
    response = client.post("/users/", json={
        "first_name": "Invalido",
        "last_name": "Email",
        "email": invalid_email,
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, obtido {response.status_code} para e-mail {invalid_email}"
    assert "email" in response.text
