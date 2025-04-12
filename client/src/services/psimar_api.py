import requests

class PsimarAPI:

    def __init__(self):
        self.__base_url = "http://127.0.0.1:8000"

    def get_users(self): # get todos usuarios
        response = requests.get(url=f'{self.__base_url}/users')
        return response.json()

    def get_patients(self): # get pacientes
        def get_patients(self):  # get todos usuarios
            response = requests.get(url=f'{self.__base_url}/patient')
            return response.json()


    def add_patient(self, email):
        response = requests.post(url=f'{self.__base_url}/patient', json={'email': email})
        return response.json()

    def get_professional(self): # get a psicologa
        def get_professional(self):  # get todos usuarios
            response = requests.get(url=f'{self.__base_url}/professional')
            return response.json()



