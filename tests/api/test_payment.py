import pytest
import uuid
from datetime import datetime, timedelta, timezone

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())


@pytest.fixture
def create_payment_payload():
    def _payload(patient_id, professional_id, appointment_id, amount=150.00, payment_method="card"):
        return {
            "patient_id": patient_id,
            "professional_id": professional_id,
            "appointment_id": appointment_id,
            "amount": amount,
            "payment_method": payment_method
        }

    return _payload


def test_make_payment(client, create_test_user, login_test_user, create_payment_payload, unique_email, unique_access_code, insert_access_code):
    # Cria paciente e faz login
    patient_id = create_test_user("Login", "User", unique_email, "123456", user_type="patient")
    token = login_test_user(unique_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Criar profissional
    professional_email = "prof" + unique_email
    code = unique_access_code
    insert_access_code(code)
    professional_id = create_test_user("Professional", "User", professional_email, "123456", user_type="professional", access_code=code)


    # cria agedamento
    future_date = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    response = client.post("/appointment/create", json={
        "date_time": future_date,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    print(response.json())

    assert response.status_code == 200
    appointment = response.json()
    appointment_id = appointment["id"]

    # Realizar pagamento
    payload = create_payment_payload(patient_id, professional_id, appointment_id)
    response = client.post("/payments/", json=payload, headers=headers)


    assert response.status_code == 200, f"Erro ao criar pagamento: {response.text}"
    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["professional_id"] == professional_id
    assert data["amount"] == payload["amount"]
    assert data["payment_method"] == payload["payment_method"]
    assert data["status"] == "pending"


def test_get_payment(client, create_test_user, login_test_user, create_payment_payload, unique_email, unique_access_code, insert_access_code):
    # Cria paciente e faz login
    patient_id = create_test_user("Login", "User", unique_email, "123456", user_type="patient")
    token = login_test_user(unique_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Criar profissional
    professional_email = "prof" + unique_email
    code1 = unique_access_code
    insert_access_code(code1)
    professional_id = create_test_user("Professional", "User", professional_email, "123456", user_type="professional",access_code=code1)

    # cria agedamento
    future_date = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    response = client.post("/appointment/create", json={
        "date_time": future_date,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    print(response.json())

    assert response.status_code == 200
    appointment = response.json()
    appointment_id = appointment["id"]

    # Criar pagamento
    payload = create_payment_payload(patient_id, professional_id, appointment_id)
    response = client.post("/payments/", json=payload, headers=headers)
    assert response.status_code == 200
    payment_id = response.json()["id"]

    # Buscar pagamento
    get_response = client.get(f"/payments/{payment_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == payment_id
    assert data["patient_id"] == patient_id
    assert data["professional_id"] == professional_id


def test_get_nonexistent_payment(client):
    response = client.get("/payments/9999")  # ID inexistente
    assert response.status_code == 404
    assert "Pagamento não encontrado" in response.text


def test_confirm_payment(client, create_test_user, login_test_user, create_payment_payload, monkeypatch, unique_email, unique_access_code, insert_access_code):
    # Mock do envio de e-mail
    async def mock_send_email(to, subject, content):
        return True

    monkeypatch.setattr("api.app.utils.email_utils.send_email", mock_send_email)

    # Cria paciente e faz login
    patient_id = create_test_user("Login", "User", unique_email, "123456", user_type="patient")
    token = login_test_user(unique_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    # Criar profissional
    professional_email = "prof" + unique_email
    code1 = unique_access_code
    insert_access_code(code1)
    professional_id = create_test_user("Professional", "User", professional_email, "123456", user_type="professional", access_code=code1)

    # cria agedamento
    future_date = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    response = client.post("/appointment/create", json={
        "date_time": future_date,
        "professional_id": professional_id,
        "patient_id": patient_id
    }, headers=headers)

    print(response.json())

    assert response.status_code == 200
    appointment = response.json()
    appointment_id = appointment["id"]

    # Criar pagamento
    payload = create_payment_payload(patient_id, professional_id, appointment_id)
    response = client.post("/payments/", json=payload, headers=headers)
    assert response.status_code == 200
    payment_id = response.json()["id"]

    # Confirmar pagamento
    confirm_response = client.post(f"/payments/{payment_id}/confirm")
    assert confirm_response.status_code == 200
    data = confirm_response.json()
    assert data["id"] == payment_id
    assert data["status"] == "completed"


def test_confirm_nonexistent_payment(client, monkeypatch):
    # Mock do envio de e-mail
    async def mock_send_email(to, subject, content):
        return True

    monkeypatch.setattr("api.app.utils.email_utils.send_email", mock_send_email)

    response = client.post("/payments/9999/confirm")
    assert response.status_code == 404
    assert "Pagamento não encontrado" in response.text