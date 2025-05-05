import pytest


@pytest.mark.usefixtures("db_reset")
def test_register_user(create_test_user):
    response = create_test_user("Teste", "User", "teste@example.com", "123456", "patient")
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["email"] == "teste@example.com", f"E-mail incorreto: {response.json()['email']}"

@pytest.mark.usefixtures("db_reset")
def test_register_user_with_duplicate_email(create_test_user):
    create_test_user("Teste", "User", "duplicado@example.com", "123456", "patient")
    response = create_test_user("Outro", "User", "duplicado@example.com", "123456", "patient")
    assert response.status_code == 400, f"Esperado 400, recebido {response.status_code}: {response.text}"
    assert response.json()["detail"] == "Email já cadastrado", f"Mensagem incorreta: {response.json()['detail']}"

@pytest.mark.usefixtures("db_reset")
def test_register_user_with_short_password(create_test_user):
    response = create_test_user("Teste", "Curto", "short@example.com", "123", "patient")
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"

@pytest.mark.usefixtures("db_reset")
def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": "incompleto@example.com",
        "senha": "123456",
        "user_type": "patient"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"

@pytest.mark.usefixtures("db_reset")
def test_register_user_invalid_user_type(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Invalido",
        "email": "tipoinvalido@example.com",
        "password": "123456",
        "user_type": "invalid_type"
    })
    assert response.status_code == 422, f"Esperado 422, recebido {response.status_code}: {response.text}"

@pytest.mark.usefixtures("db_reset")
def test_create_professional_and_check_type(client):
    response = client.post("/users/", json={
        "first_name": "Teste",
        "last_name": "Valido",
        "email": "validprof@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": "codigo123"
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"


@pytest.mark.usefixtures("db_reset")
def test_register_professional_user(client):
    response = client.post("/users/", json={
        "first_name": "Dr.",
        "last_name": "House",
        "email": "house@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": "codigo123"
    })
    assert response.status_code == 201, f"Esperado 201, recebido {response.status_code}: {response.text}"
    assert response.json()["user_type"] == "professional", f"Tipo de usuário incorreto: {response.json()['user_type']}"

@pytest.mark.usefixtures("db_reset")
def test_create_professional_without_access_code(client):
    response = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "SemCodigo",
        "email": "semcodigo@example.com",
        "password": "123456",
        "user_type": "professional"
    })
    assert response.status_code == 422 or response.status_code == 400, f"Esperado 422 ou 400, recebido {response.status_code}: {response.text}"
    assert "código de acesso" in response.text or "access code" in response.text

@pytest.mark.usefixtures("db_reset")
def test_full_flow_register_login_appointment_list(client, login_test_user):
    # Cadastro paciente e profissional
    resp1 = client.post("/users/", json={
        "first_name": "Paciente",
        "last_name": "Teste",
        "email": "pac@example.com",
        "password": "123456",
        "user_type": "patient"
    })
    assert resp1.status_code == 201, f"Erro ao criar paciente: {resp1.text}"

    resp2 = client.post("/users/", json={
        "first_name": "Profissional",
        "last_name": "Teste",
        "email": "prof@example.com",
        "password": "123456",
        "user_type": "professional",
        "access_code": "codigo123"
    })
    assert resp2.status_code == 201, f"Erro ao criar profissional: {resp2.text}"

    token = login_test_user("prof@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Agendamento
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-21T09:00:00",
        "patient_id": 1
    }, headers=headers)
    assert response.status_code == 200

    # Listagem de agendamentos
    response = client.get("/appointment/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert any(a["date_time"].startswith("2025-04-21T09:00:00") for a in data), "Agendamento não encontrado na listagem"