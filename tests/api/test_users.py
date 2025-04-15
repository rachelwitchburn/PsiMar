def test_register_user(create_user):
    response = create_user("Teste", "teste@example.com", "123456", True)
    assert response.status_code == 201
    assert response.json()["email"] == "teste@example.com"

def test_register_user_with_duplicate_email(create_user):
    create_user("Teste", "duplicado@example.com", "123456", True)
    response = create_user("Outro", "duplicado@example.com", "123456", True)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado"

def test_register_user_with_short_password(create_user):
    response = create_user("Teste", "short@example.com", "123", True)
    assert response.status_code == 422

def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": "incompleto@example.com",
        "senha": "123456"
    })
    assert response.status_code == 422

def test_register_user_invalid_user_type(client):
    response = client.post("/users/", json={
        "nome": "Teste",
        "email": "tipoinvalido@example.com",
        "senha": "123456",
        "aceitou_termos": True,
        "user_type": "invalid_type"
    })
    assert response.status_code == 422

def test_create_professional_and_check_type(client):
    response = client.post("/users/", json={
        "nome": "Profissional Valido",
        "email": "validprof@example.com",
        "senha": "123456",
        "aceitou_termos": True,
        "user_type": "professional"
    })
    assert response.status_code == 201
    assert response.json()["user_type"] == "professional"


def test_register_professional_user(client):
    response = client.post("/users/", json={
        "nome": "Dr. House",
        "email": "house@example.com",
        "senha": "123456",
        "aceitou_termos": True,
        "user_type": "professional"
    })
    assert response.status_code == 201
    assert response.json()["user_type"] == "professional"