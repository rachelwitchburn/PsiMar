import pytest
import uuid

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())[:8]

def test_list_professionals_as_patient(client, create_test_user, get_auth_token, unique_email, unique_access_code, insert_access_code):

    patient_email = "patient" + unique_email
    patient_id = create_test_user(email=patient_email, password="123456", user_type="patient")
    token = get_auth_token(patient_email, "123456")

    pro1_email = "pro1" + unique_email
    pro2_email = "pro2" + unique_email

    code1 = "123"+ unique_access_code
    insert_access_code(code1)
    code2 = "456"+ unique_access_code
    insert_access_code(code2)

    create_test_user(email=pro1_email, password="123456", user_type="professional", access_code=code1)
    create_test_user(email=pro2_email, password="123456", user_type="professional", access_code=code2)


    response = client.get(
        "/professional/list",
        headers={"Authorization": f"Bearer {token}"}
    )


    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for item in data:
        assert "id" in item
        assert "name" in item

def test_list_professionals_as_professional_forbidden(client, create_test_user, get_auth_token, unique_email, unique_access_code, insert_access_code):


    professional_email = "prof3" + unique_email
    code3 = "789" + unique_access_code
    insert_access_code(code3)
    create_test_user(email=professional_email, password="123456", user_type="professional", access_code=code3)
    token = get_auth_token(professional_email, "123456")

    response = client.get(
        "/professional/list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403, f"Esperado 403, recebido {response.status_code}: {response.text}"

def test_list_patients_as_professional(client, create_test_user, get_auth_token, unique_email, unique_access_code, insert_access_code):


    professional_email = "prof4" + unique_email
    code4 = "987" + unique_access_code
    insert_access_code(code4)
    create_test_user(email=professional_email, password="123456", user_type="professional", access_code=code4)
    token = get_auth_token(professional_email, "123456")

    create_test_user(email="pat1" + unique_email, password="123456", user_type="patient")
    create_test_user(email="pat2" +unique_email, password="123456", user_type="patient")

    response = client.get(
        "/patient/list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for item in data:
        assert "id" in item
        assert "name" in item

def test_list_patients_as_patient_forbidden(client, create_test_user, get_auth_token, unique_email, unique_access_code, insert_access_code):

    patient_email = "pat3" + unique_email
    create_test_user(email=patient_email, password="123456", user_type="patient")
    token = get_auth_token(patient_email, "123456")

    response = client.get(
        "/patient/list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403, f"Esperado 403, recebido {response.status_code}: {response.text}"