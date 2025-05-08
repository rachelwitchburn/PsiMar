"""

def test_request_appointment(client, create_test_user, login_test_user):
    patient = create_test_user("Paciente", "pac@example.com", "123456", user_type="patient").json()


    # Login como profissional (quem cria o agendamento nesse endpoint)
    token = login_test_user("pro@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/appointment/create", data={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": patient["id"]
    }, headers=headers)

    assert response.status_code == 200, f"Esperado status 200, recebido {response.status_code}: {response.text}"
    assert response.json()["status"] == "requested", f"Status esperado 'requested', recebido: {response.json()['status']}"


def test_appointment_conflict(client, create_test_user, login_test_user):
    patient = create_test_user("Paciente", "pac1@example.com", "123456", user_type="patient").json()


    token = login_test_user("prof1@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Primeiro agendamento
    client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": patient["id"]
    }, headers=headers)

    # Segundo agendamento no mesmo horário
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": patient["id"]
    }, headers=headers)

    assert response.status_code == 400, f"Esperado status 400, recebido {response.status_code}: {response.text}"
    assert "Já existe um agendamento" in response.json()["detail"], "Mensagem de conflito não encontrada"


def test_list_appointments_for_patient(client, create_test_user, login_test_user):
    patient = create_test_user("Paciente", "listpac@example.com", "123456", user_type="patient").json()

    # Login como profissional e cria agendamento
    token_prof = login_test_user("listprof@example.com", "123456")
    headers_prof = {"Authorization": f"Bearer {token_prof}"}

    client.post("/appointment/create", json={
        "date_time": "2025-04-21T10:00:00",
        "patient_id": patient["id"]
    }, headers=headers_prof)

    # Login como paciente e consulta agendamentos
    token_patient = login_test_user("listpac@example.com", "123456")
    headers_patient = {"Authorization": f"Bearer {token_patient}"}

    response = client.get("/appointment/", headers=headers_patient)

    assert response.status_code == 200, f"Esperado status 200, recebido {response.status_code}: {response.text}"
    assert len(response.json()) > 0, "Lista de agendamentos para paciente está vazia"


def test_appointment_with_invalid_patient_id(client, login_test_user):
    token = login_test_user("prof1@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-20T11:00:00",
        "patient_id": 9999
    }, headers=headers)
    assert response.status_code == 404, f"Esperado 404, obtido {response.status_code}. Detalhes: {response.json()}"


def test_appointment_without_authentication(client):
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": 1
    })
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}. Detalhes: {response.json()}"



def test_appointment_with_invalid_datetime_format(client, login_test_user, create_test_user):
    # Cria profissional e paciente
    create_test_user("Paciente", "pac1@example.com", "123456", user_type="patient")
    create_test_user("Prof", "prof1@example.com", "123456", user_type="professional", access_code="1234")

    token = login_test_user("prof1@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/appointment/create", json={
        "date_time": "20-04-2025 10:00",  # formato inválido
        "patient_id": 1
    }, headers=headers)

    assert response.status_code == 422, f"Esperado 422, obtido {response.status_code}. Detalhes: {response.text}"
    assert "date_time" in response.text, "Campo 'date_time' não reportado como inválido"



def test_conflict_different_patients_same_professional(client, login_test_user, create_test_user):
    create_test_user("Paciente1", "p1@example.com", "123456", user_type="patient")
    create_test_user("Paciente2", "p2@example.com", "123456", user_type="patient")
    create_test_user("Prof", "prof@example.com", "123456", user_type="professional", access_code="1234")

    token = login_test_user("prof@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Primeiro agendamento com Paciente 1
    r1 = client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": 1
    }, headers=headers)
    assert r1.status_code == 200, f"Esperado 200, obtido {r1.status_code}"

    # Segundo agendamento com Paciente 2, mesmo horário
    r2 = client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": 2
    }, headers=headers)
    assert r2.status_code == 409, f"Esperado 409, obtido {r2.status_code}"
    assert r2.json()["detail"] == "Já existe um agendamento para esse horário", f"Mensagem inesperada: {r2.json()}"


def test_patient_cannot_access_others_appointments(client, login_test_user, create_test_user):
    create_test_user("Paciente1", "p1@example.com", "123456", user_type="patient")
    create_test_user("Paciente2", "p2@example.com", "123456", user_type="patient")
    create_test_user("Prof", "prof@example.com", "123456", user_type="professional", access_code="1234")

    prof_token = login_test_user("prof@example.com", "123456")
    prof_headers = {"Authorization": f"Bearer {prof_token}"}

    # Cria agendamento para Paciente 1
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-20T14:00:00",
        "patient_id": 1
    }, headers=prof_headers)
    assert response.status_code == 200

    # Paciente 2 tenta acessar lista (deve ver só seus agendamentos, não os de outros)
    patient2_token = login_test_user("p2@example.com", "123456")
    patient2_headers = {"Authorization": f"Bearer {patient2_token}"}
    response = client.get("/appointment/", headers=patient2_headers)

    assert response.status_code == 200
    appointments = response.json()
    assert all(app["patient"]["email"] == "p2@example.com" for app in appointments), "Paciente 2 viu agendamentos de outro usuário"
"""