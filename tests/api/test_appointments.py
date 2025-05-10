import pytest
from datetime import datetime, timedelta
import uuid

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())[:8]

def test_request_appointment(client, create_test_user, login_test_user, unique_email, unique_access_code):
    # Cria paciente e faz login como paciente
    patient_id = create_test_user("Paciente", "User", unique_email, "123456", user_type="patient")
    token = login_test_user(unique_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Cria profissional
    professional_email = f"prof_{unique_email}"
    professional_id = create_test_user("Prof", "Example", professional_email, "123456", user_type="professional", access_code=unique_access_code)

    future_date = (datetime.now() + timedelta(days=1)).isoformat()

    response = client.post("/appointment/create", json={
        "date_time": future_date,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    print(response.json())

    assert response.status_code == 200, f"Esperado status 200, recebido {response.status_code}: {response.text}"
    response_data = response.json()
    assert response_data["status"] == "requested", f"Status esperado 'requested', recebido: {response_data['status']}"
    assert response_data["patient_id"] == patient_id, "O paciente no agendamento deve ser o usuário autenticado."
    assert response_data["professional_id"] == professional_id, "Profissional incorreto no agendamento."


def test_appointment_conflict(client, create_test_user, login_test_user, unique_email, unique_access_code):
    # Cria paciente e faz login como paciente
    patient_id = create_test_user("Paciente", "Test", unique_email, "123456", user_type="patient")
    token = login_test_user(unique_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Cria profissional
    professional_email = f"prof_{unique_email}"
    professional_id = create_test_user("Prof", "Example", professional_email, "123456", user_type="professional", access_code=unique_access_code)

    future_datetime = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()

    # Primeiro agendamento
    response = client.post("/appointment/create", json={
        "date_time": future_datetime,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    assert response.status_code == 200, f"Esperado status 200, recebido {response.status_code}: {response.text}"
    response_data = response.json()
    assert response_data["status"] == "requested", f"Status esperado 'requested', recebido: {response_data['status']}"
    assert response_data["patient_id"] == patient_id, "O paciente no agendamento deve ser o usuário autenticado."
    assert response_data["professional_id"] == professional_id, "Profissional incorreto no agendamento."

    # Segundo agendamento no mesmo horário
    response = client.post("/appointment/create", json={
        "date_time": future_datetime,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    assert response.status_code == 409, f"Esperado status 409, recebido {response.status_code}: {response.text}"
    assert "Já existe um agendamento" in response.json()["detail"], "Mensagem de conflito não encontrada"


def test_list_appointments_for_patient(client, create_test_user, login_test_user, unique_email, unique_access_code):
    # Cria paciente
    patient_id = create_test_user("Paciente", "Test", unique_email, "123456", user_type="patient")

    # Cria profissional
    prof_email = f"prof-{unique_email}"
    professional_id = create_test_user("Profissional", "Test", prof_email, "123456", user_type="professional",access_code=unique_access_code)

    # Login como paciente e cria agendamento
    token_patient = login_test_user(unique_email, "123456")
    headers_patient = {"Authorization": f"Bearer {token_patient}"}

    # Data futura para o agendamento
    future_datetime = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()

    # Solicita agendamento
    response_create = client.post("/appointment/create", json={
        "date_time": future_datetime,
        "patient_id": patient_id,
        "professional_id": professional_id
    }, headers=headers_patient)

    assert response_create.status_code == 200, f"Falha ao criar agendamento: {response_create.text}"

    # Lista agendamentos do paciente
    response = client.get("/appointment/", headers=headers_patient)

    assert response.status_code == 200, f"Esperado status 200, recebido {response.status_code}: {response.text}"
    assert len(response.json()) > 0, "Lista de agendamentos para paciente está vazia"



def test_appointment_with_invalid_patient_id(client, create_test_user, login_test_user, unique_email, unique_access_code):
    # Cria profissional para realizar o agendamento
    prof_email = unique_email
    professional_id = create_test_user("Prof", "Test", prof_email, "123456", user_type="professional", access_code=unique_access_code)

    # Faz login como profissional
    token = login_test_user(prof_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Data futura para o agendamento
    future_datetime = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()


    response = client.post("/appointment/create-professional", json={
        "date_time": future_datetime,
        "professional_id": professional_id,
        "patient_id": 9999
    }, headers=headers)
    assert response.status_code == 404, f"Esperado 404, obtido {response.status_code}. Detalhes: {response.json()}"


def test_appointment_without_authentication(client):
    response = client.post("/appointment/create", json={
        "date_time": "2025-04-20T10:00:00",
        "patient_id": 1
    })
    assert response.status_code == 401, f"Esperado 401, obtido {response.status_code}. Detalhes: {response.json()}"



def test_appointment_with_invalid_datetime_format(client, login_test_user, create_test_user, unique_email, unique_access_code):
    # Cria profissional e paciente
    patient_email = unique_email
    patient_id = create_test_user("Paciente","Teste", patient_email, "123456", user_type="patient")
    prof_email = "prof"+ unique_email  # Adiciona um prefixo para garantir unicidade
    professional_id = create_test_user("Prof","Teste", prof_email, "123456", user_type="professional", access_code=unique_access_code)

    #login como profissional
    token = login_test_user(prof_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/appointment/create-professional", json={
        "date_time": "20-04-2025 10:00",  # formato inválido
        "patient_id": patient_id,
        "professional_id": professional_id
    }, headers=headers)

    assert response.status_code == 422, f"Esperado 422, obtido {response.status_code}. Detalhes: {response.text}"
    assert "date_time" in response.text, "Campo 'date_time' não reportado como inválido"



def test_conflict_different_patients_same_professional(client, login_test_user, create_test_user, unique_email, unique_access_code):

    patient1_email = "p1"+ unique_email
    patient2_email = "p2" + unique_email
    prof_email = "prof" + unique_email

    patient1_id = create_test_user("Paciente1","Teste", patient1_email, "123456", user_type="patient")
    patient2_id = create_test_user("Paciente2","Teste", patient2_email, "123456", user_type="patient")
    professional_id = create_test_user("Prof","Teste", prof_email, "123456", user_type="professional", access_code=unique_access_code)

    # login como profissional
    token = login_test_user(prof_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Data futura para o agendamento
    future_datetime = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()

    # Primeiro agendamento com Paciente 1
    r1 = client.post("/appointment/create-professional", json={
        "date_time": future_datetime,
        "patient_id": patient1_id,
        "professional_id": professional_id
    }, headers=headers)
    assert r1.status_code == 200, f"Esperado 200, obtido {r1.status_code}"

    # Segundo agendamento com Paciente 2, mesmo horário
    r2 = client.post("/appointment/create-professional", json={
        "date_time": future_datetime,
        "patient_id": patient2_id,
        "professional_id": professional_id
    }, headers=headers)
    assert r2.status_code == 409, f"Esperado 409, obtido {r2.status_code}"
    assert r2.json()["detail"] == "Já existe um agendamento confirmado neste horário.", f"Mensagem inesperada: {r2.json()}"


def test_patient_cannot_access_others_appointments(client, login_test_user, create_test_user, unique_email, unique_access_code):

    patient1_email = "p1" + unique_email
    patient2_email = "p2" + unique_email
    prof_email = "prof" + unique_email

    patient1_id = create_test_user("Paciente1","Teste", patient1_email, "123456", user_type="patient")
    create_test_user("Paciente2", "Teste", patient2_email, "123456", user_type="patient")
    professional_id = create_test_user("Prof","Teste", prof_email, "123456", user_type="professional", access_code=unique_access_code)

    patient1_token = login_test_user(patient1_email, "123456")
    patient1_headers = {"Authorization": f"Bearer {patient1_token}"}

    # Data futura para o agendamento
    future_datetime = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()

    # Cria agendamento para Paciente 1
    response = client.post("/appointment/create", json={
        "date_time": future_datetime,
        "patient_id": patient1_id,
        "professional_id": professional_id
    }, headers=patient1_headers)
    assert response.status_code == 200

    # Paciente 2 tenta acessar lista (deve ver só seus agendamentos, não os de outros)
    patient2_token = login_test_user(patient2_email, "123456")
    patient2_headers = {"Authorization": f"Bearer {patient2_token}"}
    response = client.get("/appointment/", headers=patient2_headers)

    assert response.status_code == 200
    appointments = response.json()
    assert all(app["patient"]["email"] == patient2_email for app in appointments), "Paciente 2 viu agendamentos de outro usuário"
