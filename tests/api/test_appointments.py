def test_request_appointment(client, create_user):
    patient = create_user("Paciente", "pac@example.com", "123456", True).json()
    prof = create_user("Prof", "pro@example.com", "123456", True, user_type="professional").json()

    response = client.post("/appointments/request", json={
        "appointment_date": "2025-04-20T10:00:00",
        "patient_id": patient["id"],
        "professional_id": prof["id"],
        "requested_by": "patient"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "requested"

def test_appointment_conflict(client, create_user):
    patient = create_user("Paciente", "pac1@example.com", "123456", True).json()
    prof = create_user("Prof", "prof1@example.com", "123456", True, user_type="professional").json()

    # Primeiro agendamento
    client.post("/appointments/request", json={
        "appointment_date": "2025-04-20T10:00:00",
        "patient_id": patient["id"],
        "professional_id": prof["id"],
        "requested_by": "patient"
    })

    # Segundo agendamento no mesmo horário
    response = client.post("/appointments/request", json={
        "appointment_date": "2025-04-20T10:00:00",
        "patient_id": patient["id"],
        "professional_id": prof["id"],
        "requested_by": "patient"
    })

    assert response.status_code == 400
    assert "Já existe um agendamento" in response.json()["detail"]

def test_list_appointments_for_patient(client, create_user):
    patient = create_user("Paciente", "listpac@example.com", "123456", True).json()
    prof = create_user("Prof", "listprof@example.com", "123456", True, user_type="professional").json()

    client.post("/appointments/request", json={
        "appointment_date": "2025-04-21T10:00:00",
        "patient_id": patient["id"],
        "professional_id": prof["id"],
        "requested_by": "patient"
    })

    response = client.get(f"/appointments/patient/{patient['id']}")
    assert response.status_code == 200
    assert len(response.json()) > 0
