import pytest
import uuid
from api.app.security import create_reset_token

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("FROM_EMAIL", "test@example.com")
    monkeypatch.setenv("SMTP_USER", "test@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "fakepassword")
    monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")


def test_authenticated_reset_password(client, create_test_user, get_auth_token, unique_email):
    user_id = create_test_user("Reset", "Senha", unique_email, "123456", user_type="patient")
    token = get_auth_token(unique_email, "123456")

    response = client.post(
        "/auth/reset-password",
        json={"nova_senha": "nova_senha123"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Senha alterada com sucesso" in response.json()["message"]

    # Testa login com nova senha
    login_response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "nova_senha123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_reset_password_with_token(client, create_test_user, unique_email):
    create_test_user("Reset", "Senha", unique_email, "123456", user_type="patient")
    token = create_reset_token(email=unique_email)

    response = client.post("/auth/reset-password-with-token", json={
        "token": token,
        "nova_senha": "nova_senha123"
    })

    assert response.status_code == 200
    assert "Senha redefinida com sucesso" in response.json()["message"]

    # Testa login com nova senha
    login_response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "nova_senha123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()