import uuid
import pytest
from datetime import datetime, timedelta, timezone

@pytest.fixture
def unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.fixture
def unique_access_code():
    return str(uuid.uuid4())[:8]

@pytest.fixture
def create_task_payload():
    def _payload(patient_id, title="Atividade", description="Descrição da tarefa", due_date=None):
        return {
            "patient_id": patient_id,
            "title": title,
            "description": description,
            "due_date": due_date or (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
        }
    return _payload


def test_create_task(client, create_test_user, get_auth_token, insert_access_code, create_task_payload, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    professional_email = "prof" + unique_email
    patient_email = "patient" + unique_email

    # Cria paciente e profissional
    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=professional_email, user_type="professional", access_code=unique_access_code)

    token = get_auth_token(professional_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}

    payload = create_task_payload(patient_id, title="Título da Tarefa")
    response = client.post("/tasks/", json=payload, headers=headers)

    assert response.status_code == 201, f"Erro ao criar tarefa: {response.text}"
    data = response.json()
    assert data["title"] == "Título da Tarefa"
    assert data["description"] == payload["description"]
    assert data["status"] == "pending"

def test_list_tasks_for_patient(client, create_test_user, get_auth_token, create_task_payload, insert_access_code, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    professional_email = "prof" + unique_email
    patient_email = "patient" + unique_email

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=professional_email, user_type="professional", access_code=unique_access_code)

    # Cria tarefa com o token do profissional
    professional_token = get_auth_token(professional_email, "123456")
    prof_headers = {"Authorization": f"Bearer {professional_token}"}
    client.post("/tasks/", json=create_task_payload(patient_id, title="Título da Tarefa"), headers=prof_headers)

    # Agora paciente lista tarefas
    patient_token = get_auth_token(patient_email, "123456")
    patient_headers = {"Authorization": f"Bearer {patient_token}"}
    response = client.get("/tasks/patient", headers=patient_headers)

    assert response.status_code == 200, f"Erro ao listar tarefas: {response.text}"
    tasks = response.json()
    print(response.status_code, response.text)
    assert isinstance(tasks, list)
    assert any(task["title"] == "Título da Tarefa" for task in tasks)

def test_update_task_completion(client, create_test_user, get_auth_token, insert_access_code, create_task_payload, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    professional_email = "prof" + unique_email
    patient_email = "patient" + unique_email

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=professional_email, user_type="professional", access_code=unique_access_code)

    token = get_auth_token(professional_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}
    task = client.post("/tasks/", json=create_task_payload(patient_id), headers=headers).json()

    update_resp = client.patch(f"/tasks/{task['id']}", json={"status": "completed"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"

def test_list_assigned_tasks(client, create_test_user, get_auth_token, insert_access_code, create_task_payload, unique_email, unique_access_code):
    insert_access_code(unique_access_code)
    professional_email = "prof" + unique_email
    patient_email = unique_email

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=professional_email, user_type="professional", access_code=unique_access_code)

    # Cria tarefa com o token do profissional
    professional_token = get_auth_token(professional_email, "123456")
    prof_headers = {"Authorization": f"Bearer {professional_token}"}
    client.post("/tasks/", json=create_task_payload(patient_id, title="Título da Tarefa"), headers=prof_headers)

    # Profissional lista suas tarefas designadas
    response = client.get("/tasks/professional/assigned", headers=prof_headers)
    assert response.status_code == 200, f"Erro ao listar tarefas designadas: {response.text}"
    data = response.json()
    assert any(task["title"] == "Título da Tarefa" for task in data)

def test_patient_cannot_create_task(client, create_test_user, get_auth_token, create_task_payload, unique_email):
    patient_email = unique_email
    patient_id = create_test_user(email=patient_email, user_type="patient")
    token = get_auth_token(patient_email, "123456")

    response = client.post("/tasks/", json=create_task_payload(patient_id), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "Somente profissionais podem criar tarefas" in response.text

def test_professional_cannot_view_patient_tasks(client, create_test_user, get_auth_token, insert_access_code, unique_email, unique_access_code):
    insert_access_code(unique_access_code)
    email = unique_email
    create_test_user(email=email, user_type="professional", access_code=unique_access_code)
    token = get_auth_token(email, "123456")

    # Profissionais não devem conseguir acessar rota exclusiva de pacientes
    response = client.get("/tasks/patient", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "Somente pacientes podem ver suas tarefas" in response.text

def test_patient_cannot_update_other_patient_task(client, create_test_user, get_auth_token, insert_access_code, create_task_payload, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    prof_email = "prof" + unique_email
    patient1_email = "p1" + unique_email
    patient2_email = "p2" + unique_email

    patient1_id = create_test_user(email=patient1_email, user_type="patient")
    create_test_user(email=patient2_email, user_type="patient")
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)

    prof_token = get_auth_token(prof_email, "123456")
    task = client.post("/tasks/", json=create_task_payload(patient1_id), headers={"Authorization": f"Bearer {prof_token}"}).json()


    # paciente 2 tenta atualizar tarefa de paciente 1
    patient2_token = get_auth_token(patient2_email, "123456")
    response = client.patch(f"/tasks/{task['id']}", json={"status": "completed"}, headers={"Authorization": f"Bearer {patient2_token}"})


    assert response.status_code == 403
    assert "Não autorizado" in response.text
    assert "tarefas" not in response.text.lower()

def test_update_nonexistent_task(client, create_test_user, get_auth_token, insert_access_code, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    email = unique_email
    create_test_user(email=email, user_type="professional", access_code=unique_access_code)
    token = get_auth_token(email, "123456")

    response = client.patch("/tasks/9999", json={"status": "completed"}, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert "Tarefa não encontrada" in response.text

def test_create_task_missing_title(client, create_test_user, get_auth_token, insert_access_code, unique_email,unique_access_code):
    insert_access_code(unique_access_code)
    prof_email = "prof" + unique_email
    patient_email = unique_email
    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)

    token = get_auth_token(prof_email, "123456")

    payload = {
        "patient_id": patient_id,
        "description": "Descrição da tarefa",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    }

    response = client.post("/tasks/", json=payload, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 422
    assert any("title" in err["loc"] for err in response.json()["detail"])

def test_professional_cannot_update_others_task(client, create_test_user, get_auth_token, insert_access_code, create_task_payload, unique_email,unique_access_code):
    code1 = unique_access_code
    code2 = unique_access_code + "2"
    insert_access_code(code1)
    insert_access_code(code2)
    prof1_email = "prof1" + unique_email
    prof2_email = "prof2" + unique_email
    patient_email = unique_email

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=prof1_email, user_type="professional", access_code=code1)
    create_test_user(email=prof2_email, user_type="professional", access_code=code2)

    token_prof1 = get_auth_token(prof1_email, "123456")
    task = client.post("/tasks/", json=create_task_payload(patient_id), headers={"Authorization": f"Bearer {token_prof1}"}).json()


    token_prof2 = get_auth_token(prof2_email, "123456")
    response = client.patch(f"/tasks/{task['id']}", json={"status": "completed"}, headers={"Authorization": f"Bearer {token_prof2}"})

    assert response.status_code == 403
    assert "Não autorizado" in response.text



def test_patient_can_get_own_task_by_id(client, create_test_user, get_auth_token, create_task_payload, unique_email, insert_access_code, unique_access_code):
    patient_email = unique_email
    prof_email = "prof" + unique_email
    insert_access_code(unique_access_code)

    patient_id = create_test_user(email=patient_email, user_type="patient")

    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)
    prof_token = get_auth_token(prof_email, "123456")

    # Cria a tarefa com o profissional
    payload = create_task_payload(patient_id)
    response = client.post("/tasks/", json=payload, headers={"Authorization": f"Bearer {prof_token}"})
    task = response.json()

    # Paciente obtém a tarefa
    token = get_auth_token(patient_email, "123456")



    response = client.get(f"/tasks/{task['id']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == task["id"]

def test_professional_can_delete_own_task(client, create_test_user, get_auth_token, create_task_payload, insert_access_code, unique_email, unique_access_code):
    prof_email = "prof" + unique_email
    patient_email = unique_email
    insert_access_code(unique_access_code)

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)

    token = get_auth_token(prof_email, "123456")
    headers = {"Authorization": f"Bearer {token}"}
    payload = create_task_payload(patient_id)

    response = client.post("/tasks/", json=payload, headers=headers)
    task = response.json()

    # Exclui a tarefa
    delete_response = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert delete_response.status_code == 204


def test_patient_cannot_delete_task(client, create_test_user, get_auth_token, create_task_payload, unique_email, insert_access_code, unique_access_code):
    insert_access_code(unique_access_code)
    prof_email = "prof" + unique_email
    patient_email = unique_email

    # Criação dos usuários
    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)

    # Profissional cria a tarefa
    prof_token = get_auth_token(prof_email, "123456")
    task = client.post("/tasks/", json=create_task_payload(patient_id), headers={"Authorization": f"Bearer {prof_token}"}).json()

    # Paciente tenta deletar a tarefa
    patient_token = get_auth_token(patient_email, "123456")
    response = client.delete(f"/tasks/{task['id']}", headers={"Authorization": f"Bearer {patient_token}"})

    assert response.status_code == 403
    assert "Somente profissionais podem excluir tarefas." in response.text

def test_wrong_patient_cannot_update_task(client, create_test_user, get_auth_token, create_task_payload, unique_email, insert_access_code, unique_access_code):
    # Criar profissional e paciente correto
    prof_email = "prof" + unique_email
    correct_patient_email = unique_email
    patient = create_test_user(email=correct_patient_email, user_type="patient")
    insert_access_code(unique_access_code)
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)
    token_prof = get_auth_token(prof_email, "123456")

    # Criar a tarefa com a API (gera o ID)
    task_payload = create_task_payload(patient_id=patient)
    response = client.post("/tasks/", json=task_payload, headers={"Authorization": f"Bearer {token_prof}"})
    assert response.status_code == 201, f"Erro ao criar tarefa: {response.json()}"
    task = response.json()

    # Outro paciente tentando alterar
    other_email = "p2" + unique_email
    create_test_user(email=other_email, user_type="patient")
    token = get_auth_token(other_email, "123456")

    response = client.patch(f"/tasks/{task['id']}", headers={"Authorization": f"Bearer {token}"}, json={"status": "completed"})

    assert response.status_code == 403
    assert "Não autorizado a acessar essa tarefa." in response.text

def test_cannot_create_task_with_past_due_date(client, create_test_user, get_auth_token, insert_access_code, unique_email, unique_access_code):
    insert_access_code(unique_access_code)
    prof_email = "prof" + unique_email
    patient_email = unique_email

    patient_id = create_test_user(email=patient_email, user_type="patient")
    create_test_user(email=prof_email, user_type="professional", access_code=unique_access_code)

    token = get_auth_token(prof_email, "123456")
    past_date = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    payload = {
        "patient_id": patient_id,
        "title": "Tarefa com data passada",
        "description": "Descrição",
        "due_date": past_date
    }

    response = client.post("/tasks/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422 or response.status_code == 400
    assert "data" in response.text.lower() or "inválida" in response.text.lower()