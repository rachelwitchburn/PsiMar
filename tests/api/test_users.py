import pytest
from datetime import datetime, timedelta
import uuid
"""
@pytest.fixture
def test_register_user(create_test_user):
    response = create_test_user("Teste", "User", "teste@example.com", "123456", "patient")
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["email"] == "teste@example.com", f"E-mail incorreto: {response.json()['email']}"


def test_register_user_with_duplicate_email(create_test_user):
    create_test_user("Teste", "User", "duplicado@example.com", "123456", "patient")
    response = create_test_user("Outro", "User", "duplicado@example.com", "123456", "patient")
    assert response.status_code == 400, f"Esperado 400, recebido {response.status_code}: {response.text}"
    assert response.json()["detail"] == "Email já cadastrado", f"Mensagem incorreta: {response.json()['detail']}"


def test_register_user_with_short_password(create_test_user):
    response = create_test_user("Teste", "Curto", "short@example.com", "123", "patient")
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert "A senha deve ter pelo menos 6 caracteres" in response.text


def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": "incompleto@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"
    assert "field required" in response.text, "Mensagem de campo obrigatório não encontrada"


def test_register_user_invalid_user_type(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Invalido",
        "email": "tipoinvalido@example.com",
        "password": "123456",
        "user_type": "invalid_type"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"


def test_create_professional_and_check_type(client, insert_access_code):
    insert_access_code("codigo111")
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Valido",
        "email": "validprof@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": "codigo111"
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"



def test_register_professional_user(client, insert_access_code):
    insert_access_code("codigo222")

    response = client.post("/users/", json={
        "first_name": "Dr.",
        "last_name": "House",
        "email": "house@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": "codigo222"
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"


def test_create_professional_without_access_code(client):
    response = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "SemCodigo",
        "email": "semcodigo@example.com",
        "password": "123456",
        "user_type": "professional"
    })
    assert response.status_code in [400, 422], f"Esperado 422 ou 400, recebido {response.status_code}: {response.text}"
    assert "access_code" in response.text or "código de acesso" in response.text
"""

def test_full_flow_register_login_appointment_list(client, login_test_user, insert_access_code):
    code = f"codigo-{uuid.uuid4()}"
    insert_access_code(code)
    # Cadastro paciente
    resp1 = client.post("/users/", json={
        "first_name": "Paciente",
        "last_name": "Teste",
        "email": "pac@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert resp1.status_code == 201, f"Erro ao criar paciente: {resp1.text}"
    patient_id = resp1.json()["id"]

    # Cadastro profissional
    resp2 = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "Teste",
        "email": "prof@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": code
    })
    assert resp2.status_code == 201, f"Erro ao criar profissional: {resp2.text}"

    professional_id = resp2.json()["id"]
    token = login_test_user("prof@example.com", "123456")
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
