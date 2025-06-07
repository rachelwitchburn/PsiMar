import pytest
import uuid

@pytest.fixture
def unique_feedback_text():
    return f"Excelente atendimento {uuid.uuid4()}"

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())[:8]


def test_patient_can_send_feedback(client, create_test_user, login_test_user, unique_feedback_text, unique_email,unique_access_code, insert_access_code):

    # Criar profissional
    prof_email = "prof" + unique_email
    code = unique_access_code
    insert_access_code(code)
    professional_id = create_test_user("Professional", "User", prof_email, "123456", user_type="professional", access_code=code)

    # Criar paciente
    patient_email = "patient" + unique_email
    patient_password = "123456"
    patient_id = create_test_user("Patient", "User", patient_email, patient_password, user_type="patient")

    token = login_test_user(patient_email, patient_password)

    feedback_data = {
        "professional_id": professional_id,
        "patient_id": patient_id,
        "message": unique_feedback_text,
        "rating": 5
    }

    response = client.post(
        "/feedback/",
        json=feedback_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["message"] == unique_feedback_text


def test_professional_can_view_received_feedback(client, create_test_user, login_test_user, unique_feedback_text, unique_email, unique_access_code, insert_access_code):

    # Criar profissional
    prof_email = "prof" + unique_email
    code = unique_access_code
    insert_access_code(code)
    professional_id = create_test_user("Professional", "User", prof_email, "123456", user_type="professional", access_code=code)

    # Criar paciente
    patient_email = "patient" + unique_email
    patient_password = "123456"
    patient_id = create_test_user("Patient", "User", patient_email, patient_password, user_type="patient")

    # Paciente faz login e envia feedback
    patient_token = login_test_user(patient_email, patient_password)


    feedback_data = {
        "professional_id": professional_id,
        "patient_id": patient_id,
        "message": unique_feedback_text,
        "rating": 4
    }


    # Paciente envia feedback
    response = client.post(
        "/feedback/",
        json=feedback_data,
        headers={"Authorization": f"Bearer {patient_token}"}
    )

    assert response.status_code == 201

    # Profissional faz login e busca feedbacks recebidos
    prof_token = login_test_user(prof_email, "123456")

    # Profissional visualiza feedbacks recebidos
    response = client.get(
        f"/feedback/professional/{professional_id}",
        headers={"Authorization": f"Bearer {prof_token}"}
    )

    assert response.status_code == 200
    feedbacks = response.json()
    assert any(f["message"] == unique_feedback_text for f in feedbacks)


def test_patient_cannot_send_invalid_feedback(client, create_test_user, login_test_user, unique_email, unique_access_code, insert_access_code):

    # Criar paciente
    patient_email = "patient" + unique_email
    patient_password = "123456"
    patient_id = create_test_user("Patient", "User", patient_email, patient_password, user_type="patient")

    token = login_test_user(patient_email, patient_password)

    # Dados inválidos: falta professional_id e rating
    invalid_feedback_data = {
        "message": "Feedback sem profissional"
    }


    response = client.post(
        "/feedback/",
        json=invalid_feedback_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422  # Unprocessable Entity
