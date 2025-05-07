import pytest
"""

def test_register_user_success(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Usuario",
        "email": "teste@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 201, f"Esperado status 201, recebido {response.status_code}: {response.text}"
    assert response.json()["email"] == "teste@example.com"


def test_successful_login(client, create_test_user):
    create_test_user("Login", "User", "login@example.com", "123456", user_type="patient")
    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "123456"
    })
    assert response.status_code == 200, f"Esperado 200, recebido {response.status_code}: {response.text}"
    assert "access_token" in response.json()


def test_login_wrong_password(client, create_test_user):
    create_test_user("Wrong", "Pass", "wrong@example.com", "123456", user_type="patient")
    response = client.post("/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401, f"Esperado 401, recebido {response.status_code}: {response.text}"
    assert "incorretos" in response.json()["detail"]


def test_register_user_with_short_password(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Curta",
        "email": "senhaCurta@example.com",
        "password": "123",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert any("senha" in d.get("msg", "") for d in response.json()["detail"]), "Mensagem de senha curta não encontrada"


def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": "incompleto@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert any("field required" in d["msg"] for d in response.json()["detail"])


def test_login_nonexistent_email(client):
    response = client.post("/auth/login", data={
        "username": "naoexiste@example.com",
        "password": "123456"
    })
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}. Detalhes: {response.json()}"
    assert "incorretos" in response.json()["detail"]


def test_login_with_empty_password(client, create_test_user):
    create_test_user("Teste", "Vazio", "vazio@example.com", "123456", user_type="patient")
    response = client.post("/auth/login", data={
        "username": "vazio@example.com",
        "password": ""
    })
    assert response.status_code == 422, f"Esperado 422, obtido {response.status_code}. Detalhes: {response.text}"
    assert "password" in response.text


def test_access_with_invalid_token(client):
    response = client.get("/appointment/")
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}"
    assert "Não autorizado" in response.json()["detail"]


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
"""