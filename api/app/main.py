from fastapi import FastAPI  # Importando a classe FastAPI do FastAPI para criar o aplicativo

#se aberto do projeto_gerencia
from api.app.routers import users_router, auth_router, schedule_router, professional_router, patient_router, appointment_router

# Criação da aplicação FastAPI com título personalizado
# A classe FastAPI é a base da nossa aplicação web.
app = FastAPI(title="PSIMAR - Atendimento Psicológico")

# Incluir rotas da API para usuários e autenticação
# Aqui estamos incluindo os routers que serão responsáveis pelas rotas da API.
# O router 'users' gerencia tudo relacionado aos usuários e o router 'auth' gerencia as rotas de autenticação.
app.include_router(appointment_router.router)
app.include_router(auth_router.router)
app.include_router(patient_router.router)
app.include_router(professional_router.router)
app.include_router(schedule_router.router)
app.include_router(users_router.router)


# Rota inicial para testar o funcionamento da API
@app.get("/")
def root():
    return {"message": "API PSIMAR está rodando!"}
# Definindo uma rota simples para verificar se a API está funcionando corretamente.
@app.get("/professionalHome")
def professional_home():
    return {"message": "Bem-vindo, Maria"}

@app.get("/patientHome")
def patient_home():
    return {"message": "Bem-vindo, {patient_name}"}

@app.post("/login")
def login():
    return {"message": "Login endpoint em construção"}

