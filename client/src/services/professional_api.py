import requests

class PsimarAPI:

    def __init__(self, token=None):
        self.__base_url = "http://127.0.0.1:8000"
        self.token = token

    def _get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}


    def get_users(self):
        """
        Retorna todos os usuários (requer autenticação).
        """
        response = requests.get(f"{self.__base_url}/users", headers=self._get_headers())
        return response

    def login(self, email: str, password: str):
        """
        Realiza login e armazena o token JWT.
        """
        response = requests.post(f"{self.__base_url}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        return response

    def register_user(self, user_data: dict):
        """
        Registra um novo usuário (paciente ou psicólogo).
        """
        response = requests.post(f"{self.__base_url}/users", json=user_data)
        return response

    def get_patients(self):
        """
        Retorna todos os pacientes cadastrados.
        """
        response = requests.get(f"{self.__base_url}/patient/list", headers=self._get_headers())
        return response

    def get_professionals(self):
        """
        Retorna todos os psicologos cadastrados.
        """
        response = requests.get(f"{self.__base_url}/professional/list", headers=self._get_headers())
        return response

    def add_patient(self, email: str):
        """
        Adiciona um novo paciente (etapa 1 - e-mail).
        """
        response = requests.post(f"{self.__base_url}/patient", json={"email": email}, headers=self._get_headers())
        return response

    def login_professional(self, code):
        response = requests.post(url=f'{self.__base_url}/professional/login', json={'access_code': code})
        return response.json()

    def login_patient(self, email, password):
        response = requests.post(url=f'{self.__base_url}/patient/login', json={'email': email, 'password': password})
        return response.json()

    def reset_password(self, new_password):
        """
        Redefine a senha do usuário autenticado.
        """
        # Se for string, converte para dict, se já for dict, usa diretamente
        payload = {"nova_senha": new_password} if isinstance(new_password, str) else new_password

        response = requests.post(
            f"{self.__base_url}/auth/reset-password",
            json=payload,
            headers=self._get_headers()
        )
        return response

# feedback::
    def send_feedback(self, patient_id: int, professional_id: int, message: str):
        payload = {
            "message": message,
            "patient_id": patient_id,
            "professional_id": professional_id
        }
        response = requests.post(
            f"{self.__base_url}/feedback",
            json=payload,
            headers=self._get_headers()
        )
        return response

    def get_feedback_for_professional(self, professional_id: int):
        response = requests.get(
            f"{self.__base_url}/feedback/professional/{professional_id}",
            headers=self._get_headers()
        )
        return response

    def create_appointment(self, professional_id: int, patient_id: int, date_time: str):
        return requests.post(
            f"{self.__base_url}/appointment/create",
            json={
                "professional_id": professional_id,
                "patient_id": patient_id,
                "date_time": date_time
            },
            headers=self._get_headers()
        )

    def create_appointment_professional(self, professional_id: int, patient_id: int, date_time: str):
        return requests.post(
            f"{self.__base_url}/appointment/create-professional",
            json={
                "professional_id": professional_id,  # Adicionado
                "patient_id": patient_id,
                "date_time": date_time
            },
            headers=self._get_headers()
        )

    def get_appointments(self):
        """
        Retorna os agendamentos do usuário logado (paciente ou profissional).
        """
        response = requests.get(
            f"{self.__base_url}/appointment/",
            headers=self._get_headers()
        )
        return response

    def confirm_appointment_by_professional(self, appointment_id: int):
        """
        Profissional confirma um agendamento solicitado.
        """
        response = requests.post(
            f"{self.__base_url}/appointment/confirm-professional/{appointment_id}",
            headers=self._get_headers()
        )
        return response

    def confirm_appointment_by_patient(self, appointment_id: int):
        """Confirma agendamento como paciente"""
        return requests.post(
            f"{self.__base_url}/appointment/confirm/{appointment_id}",
            headers=self._get_headers()
        )

    def create_task(self, task_data: dict):
        """Cria uma nova tarefa para um paciente"""
        return requests.post(
            f"{self.__base_url}/tasks/",
            json=task_data,
            headers=self._get_headers()
        )

    def get_assigned_tasks(self):
        """
        Retorna todas as tarefas atribuídas pelo profissional logado.
        Requer que o usuário esteja autenticado como profissional.
        """
        response = requests.get(
            f"{self.__base_url}/tasks/professional/assigned",
            headers=self._get_headers()
        )
        return response

    def get_patient_tasks(self):
        """
        Retorna todas as tarefas atribuídas ao paciente logado.
        Requer que o usuário esteja autenticado como paciente.
        """
        response = requests.get(
            f"{self.__base_url}/tasks/patient",
            headers=self._get_headers()
        )
        return response

    def update_task_status(self, task_id: int, status: str):
        """
        Atualiza o status de uma tarefa
        """
        response = requests.patch(
            f"{self.__base_url}/tasks/{task_id}",
            json={"status": status},
            headers=self._get_headers()
        )
        return response

    def create_payment(self, payment_data: dict):
        """Envia um novo pagamento para a API"""
        return requests.post(
            f"{self.__base_url}/payments/",
            json=payment_data,
            headers=self._get_headers()
        )

    def get_payments(self):
        """Obtém todos os pagamentos do usuário logado"""
        return requests.get(
        f"{self.__base_url}/payments/",
        headers=self._get_headers()
    )

    def confirm_payment(self, payment_id: int):
        """Confirma um pagamento na API"""
        return requests.post(
            f"{self.__base_url}/payments/{payment_id}/confirm",
            json={"status": "completed"},
            headers=self._get_headers()
        )

    def get_current_user(self):
        """
        Retorna os dados do usuário atualmente autenticado.
        """
        response = requests.get(
            f"{self.__base_url}/users/me",
            headers=self._get_headers()
        )
        return response

