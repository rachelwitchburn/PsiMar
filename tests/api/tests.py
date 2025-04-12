import os
import sys
import pytest
from fastapi.testclient import TestClient
from api.app.main import app  # Garantir que a importação do 'app' seja reconhecida

# Ajustando o sys.path para garantir que a pasta 'api' seja encontrada
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../api')))

# Inicializando o TestClient com a app
client = TestClient(app)  # Use o 'app' importado aqui

# Verificando o sys.path
print("sys.path:", sys.path)



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

# Fixture para login e obtenção de token JWT
@pytest.fixture
def login_and_get_token():
    def _login(email, senha):
        response = client.post("/auth/token", data={
            "username": email,
            "password": senha
        })
        return response.json()["access_token"]
    return _login


# Fixture para criar um psicólogo (admin)
@pytest.fixture
def create_admin_user():
    def _create_admin_user():
        response = client.post("/users/", json={
            "nome": "Psicólogo",
            "email": "psicologo@example.com",
            "senha": "123456",
            "confirmacao_senha": "123456",
            "aceitou_termos": True,
            "is_admin": True
        })
        return response
    return _create_admin_user


# Fixture para criar um paciente (não-admin)
@pytest.fixture
def create_patient_user():
    def _create_patient_user():
        response = client.post("/users/", json={
            "nome": "Paciente",
            "email": "paciente@example.com",
            "senha": "123456",
            "confirmacao_senha": "123456",
            "aceitou_termos": True
        })
        return response
    return _create_patient_user

def test_criar_disponibilidade_com_admin(create_admin_user, login_and_get_token):
    create_admin_user()
    token = login_and_get_token("psicologo@example.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/disponibilidades/", json={
        "dia_semana": "segunda-feira",
        "horario_inicio": "09:00",
        "horario_fim": "17:00"
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["dia_semana"] == "segunda-feira"

    def test_paciente_nao_pode_criar_disponibilidade(create_patient_user, login_and_get_token):
        create_patient_user()
        token = login_and_get_token("paciente@example.com", "123456")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post("/disponibilidades/", json={
            "dia_semana": "terça-feira",
            "horario_inicio": "10:00",
            "horario_fim": "16:00"
        }, headers=headers)

        assert response.status_code == 403
        assert response.json()["detail"] == "Apenas administradores podem cadastrar disponibilidades"

        def test_listar_disponibilidades_publicamente(create_admin_user, login_and_get_token, create_patient_user):
            # Cria psicólogo e disponibilidade
            create_admin_user()
            token_admin = login_and_get_token("psicologo@example.com", "123456")
            headers_admin = {"Authorization": f"Bearer {token_admin}"}

            response_disponibilidade = client.post("/disponibilidades/", json={
                "dia_semana": "quarta-feira",
                "horario_inicio": "08:00",
                "horario_fim": "12:00"
            }, headers=headers_admin)
            assert response_disponibilidade.status_code == 201

            psicologo_id = response_disponibilidade.json()["psicologo_id"]

            # Cria paciente e usa o token dele
            create_patient_user()
            token_paciente = login_and_get_token("paciente@example.com", "123456")
            headers_paciente = {"Authorization": f"Bearer {token_paciente}"}

            # Consulta as disponibilidades do psicólogo
            response = client.get(f"/disponibilidades/psicologo/{psicologo_id}", headers=headers_paciente)

            assert response.status_code == 200
            assert isinstance(response.json(), list)
            assert len(response.json()) >= 1


def test_agendar_consulta(create_user):
    # Criando o usuário paciente
    paciente_response = create_user("Paciente Teste", "paciente@example.com", "123456", True)
    paciente_id = paciente_response.json()["id"]

    # Criando a disponibilidade do psicólogo
    psicologo_response = create_user("Psicólogo Teste", "psicologo@example.com", "123456", True)
    psicologo_id = psicologo_response.json()["id"]
    disponibilidade_data = {
        "dia_semana": "segunda-feira",
        "horario_inicio": "09:00:00",
        "horario_fim": "12:00:00",
    }
    disponibilidade_response = client.post(f"/disponibilidade/{psicologo_id}", json=disponibilidade_data)
    disponibilidade_id = disponibilidade_response.json()["id"]

    # Agendando a consulta
    agendamento_data = {
        "paciente_id": paciente_id,
        "disponibilidade_id": disponibilidade_id
    }
    agendamento_response = client.post("/agendar/", json=agendamento_data)
    assert agendamento_response.status_code == 200
    assert agendamento_response.json()["paciente_id"] == paciente_id
    assert agendamento_response.json()["disponibilidade_id"] == disponibilidade_id