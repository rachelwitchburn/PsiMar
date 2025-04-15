def test_register_user(client, create_user):
    response = create_user("Teste", "teste@example.com", "123456", True)
    assert response.status_code == 201
    assert response.json()["email"] == "teste@example.com"

def test_successful_login(client, create_user):
    create_user("Login User", "login@example.com", "123456", True)
    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_user_with_duplicate_email(client, create_user):
    create_user("Teste", "duplicado@example.com", "123456", True)
    response = create_user("Outro Teste", "duplicado@example.com", "123456", True)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado"

def test_login_wrong_password(client, create_user):
    create_user("Wrong Pass", "wrong@example.com", "123456", True)
    response = client.post("/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "E-mail ou senha incorretos"

def test_register_user_with_short_password(client):
    response = client.post("/users/", json={
        "nome": "Teste",
        "email": "senhaCurta@example.com",
        "senha": "123",
        "aceitou_termos": True
    })
    assert response.status_code == 422
    assert "A senha deve ter pelo menos 6 caracteres." in response.json()["detail"]

def test_register_user_missing_required_field(client):
    response = client.post("/users/", json={
        "email": "incompleto@example.com",
        "senha": "123456"
    })
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"]
