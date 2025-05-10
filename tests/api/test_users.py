import pytest
from datetime import datetime, timedelta
import uuid

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())[:8]

def test_register_user(client, unique_email):
    payload = {
        "first_name": "Teste",
        "last_name": "User",
        "email": unique_email,
        "password": "123456",
        "user_type": "patient"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert data["first_name"] == "Teste"
    assert data["user_type"] == "patient"

def test_register_user_with_duplicate_email(client, unique_email):
    payload = {
        "first_name": "Teste",
        "last_name": "User",
        "email": unique_email,
        "password": "123456",
        "user_type": "patient"
    }
    # Primeira criação deve funcionar
    response1 = client.post("/users/", json=payload)
    assert response1.status_code == 201

    # Segunda criação deve falhar
    response2 = client.post("/users/", json=payload)
    assert response2.status_code == 400
    assert "email" in response2.text.lower()


def test_register_user_with_short_password(client, unique_email):
    payload = {
        "first_name": "Teste",
        "last_name": "Curto",
        "email": unique_email,
        "password": "123",  # Senha muito curta (menos de 6 caracteres)
        "user_type": "patient"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert "password" in response.text.lower()

def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": f"{uuid.uuid4()}@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert any("Field required" in error["msg"] for error in response.json()["detail"]), "Mensagem de campo obrigatório não encontrada"

def test_register_user_invalid_user_type(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Invalido",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "123456",
        "user_type": "invalid_type"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"

def test_create_professional_and_check_type(client, insert_access_code, unique_access_code):
    email = f"{uuid.uuid4()}@example.com"
    insert_access_code(unique_access_code)
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Valido",
        "email": email,
        "password": "123456",
        "user_type": "professional",
        "access_code": unique_access_code
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"

def test_register_professional_user(client, insert_access_code, unique_access_code):
    email = f"{uuid.uuid4()}@example.com"
    insert_access_code(unique_access_code)

    response = client.post("/users/", json={
        "first_name": "Dr.",
        "last_name": "House",
        "email": email,
        "password": "123456",
        "user_type": "professional",
        "access_code": unique_access_code
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"

def test_create_professional_without_access_code(client):
    response = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "SemCodigo",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "123456",
        "user_type": "professional"
    })
    assert response.status_code in [400, 422], f"Esperado 422 ou 400, recebido {response.status_code}: {response.text}"
    assert "access_code" in response.text or "código de acesso" in response.text

def test_full_flow_register_login_appointment_list(client, login_test_user, insert_access_code):
    code = f"codigo-{uuid.uuid4()}"
    insert_access_code(code)

    email_paciente = f"{uuid.uuid4()}@example.com"
    email_profissional = f"{uuid.uuid4()}@example.com"

    # Cadastro paciente
    resp1 = client.post("/users/", json={
        "first_name": "Paciente",
        "last_name": "Teste",
        "email": email_paciente,
        "password": "123456",
        "user_type": "patient"
    })
    assert resp1.status_code == 201, f"Erro ao criar paciente: {resp1.text}"
    patient_id = resp1.json()["id"]

    # Cadastro profissional
    resp2 = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "Teste",
        "email": email_profissional,
        "password": "123456",
        "user_type": "professional",
        "access_code": code
    })
    assert resp2.status_code == 201, f"Erro ao criar profissional: {resp2.text}"
    professional_id = resp2.json()["id"]

    token = login_test_user(email_profissional, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    future_date = (datetime.now() + timedelta(days=1)).isoformat()

    # Agendamento
    response = client.post("/appointment/create-professional", json={
        "date_time": future_date,
        "patient_id": patient_id,
        "professional_id": professional_id
    }, headers=headers)
    assert response.status_code == 200, f"Erro no agendamento: {response.text}"

    # Listagem de agendamentos
    response = client.get("/appointment/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    expected_prefix = future_date[:16]
    assert any(a["date_time"].startswith(expected_prefix) for a in data), f"Agendamento com data iniciando por '{expected_prefix}' não encontrado na listagem. Dados retornados: {data}"