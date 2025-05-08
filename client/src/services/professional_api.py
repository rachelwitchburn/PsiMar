import requests

class PsimarAPI:

    def __init__(self):
        self.__base_url = "http://127.0.0.1:8000"
        self.token = None

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

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

    def register_professional(self, email: str, password: str):
        """
        Registra um novo profissional (etapa 1).
        """
        response = requests.post(f"{self.__base_url}/professional", json={"email": email, "password": password})
        return response

    def get_patients(self):
        """
        Retorna todos os pacientes cadastrados.
        """
        response = requests.get(f"{self.__base_url}/patient", headers=self._get_headers())
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

    def reset_password(self, new_password: str):
        """
        Redefine a senha do usuário autenticado.
        """
        response = requests.post(f"{self.__base_url}/auth/reset-password", json={"nova_senha": new_password},
                                 headers=self._get_headers())
        return response
