import sys
import os
from fastapi.testclient import TestClient  # Importando o cliente de teste da FastAPI
from api.app import app  # Importando a aplicação FastAPI
import pytest

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


print("sys.path:", sys.path)  # Verifique os caminhos de importação



client = TestClient(app)  # Criando um cliente para enviar requisições para a aplicação



# Criando um fixture para usuários para evitar repetição de código
@pytest.fixture
def create_user():
    def _create_user(nome, email, senha, aceitou_termos):
        return client.post("/users/", json={
            "nome": nome,
            "email": email,
            "senha": senha,
            "aceitou_termos": aceitou_termos
        })

    return _create_user


# Função de teste para registrar um usuário
def test_register_user(create_user):
    response = create_user("Teste", "teste@example.com", "123456", True)
    assert response.status_code == 201  # Espera status 201 de criação
    assert response.json()["email"] == "teste@example.com"  # Verifica se o e-mail retornado é o mesmo enviado


# Teste de cadastro de usuário com email duplicado
def test_register_user_with_duplicate_email(create_user):
    # Criação do primeiro usuário
    create_user("Teste", "duplicado@example.com", "123456", True)

    # Tentativa de criar outro usuário com o mesmo email
    response = create_user("Outro Teste", "duplicado@example.com", "123456", True)
    assert response.status_code == 400  # Espera erro devido ao email duplicado
    assert response.json()["detail"] == "Email já cadastrado"


# Teste de validação de senha curta
def test_register_user_with_short_password(create_user):
    response = create_user("Teste", "senhaCurta@example.com", "123", True)  # Senha muito curta
    assert response.status_code == 422  # Erro de validação
    assert "A senha deve ter pelo menos 6 caracteres." in response.json()["detail"]


# Teste de aceitação de termos
def test_register_user_without_accepting_terms(create_user):
    response = create_user("Teste", "semTermos@example.com", "123456", False)  # Não aceitou os termos
    assert response.status_code == 400  # Espera erro de termos não aceitos
    assert response.json()["detail"] == "Os termos devem ser aceitos para cadastro."


# Teste de falta de um campo obrigatório
def test_register_user_missing_required_field(create_user):
    response = client.post("/users/", json={
        "nome": "Teste Incompleto",
        "email": "incompleto@example.com",
        "senha": "123456"
        # 'aceitou_termos' não está incluído
    })
    assert response.status_code == 422  # Espera erro devido à falta do campo aceitou_termos
    assert "field required" in response.json()["detail"][0]["msg"]  # Verifica que o erro menciona "campo obrigatório"


# Teste de usuário administrador
def test_register_admin_user(create_user):
    response = create_user("Admin Teste", "admin@example.com", "123456", True)
    user_data = response.json()
    assert user_data[
               "is_admin"] == False  # Verifica se o valor padrão é False para is_admin (a não ser que seja alterado)


# Teste de criação de usuário com campo `is_admin` explícito
def test_register_user_with_admin(create_user):
    response = client.post("/users/", json={
        "nome": "Admin",
        "email": "adminexplicit@example.com",
        "senha": "123456",
        "aceitou_termos": True,
        "is_admin": True  # Explicitamente definindo o campo is_admin
    })
    user_data = response.json()
    assert user_data["is_admin"] == True  # Verifica se o campo 'is_admin' foi configurado corretamente

