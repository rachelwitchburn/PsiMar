from fastapi import FastAPI  # Importando a classe FastAPI do FastAPI para criar o aplicativo

#se aberto do projeto_gerencia
from api.app.routers import users, auth

# Criação da aplicação FastAPI com título personalizado
# A classe FastAPI é a base da nossa aplicação web.
app = FastAPI(title="PSIMAR - Atendimento Psicológico")

# Incluir rotas da API para usuários e autenticação
# Aqui estamos incluindo os routers que serão responsáveis pelas rotas da API.
# O router 'users' gerencia tudo relacionado aos usuários e o router 'auth' gerencia as rotas de autenticação.
app.include_router(users.router)
app.include_router(auth.router)

# Rota inicial para testar o funcionamento da API
# Definindo uma rota simples para verificar se a API está funcionando corretamente.
@app.get("/professionalHome")
def home():
    # Retorna uma mensagem simples como resposta quando o endpoint "/" for acessado.
    return {"message": "Bem-vindo, Maria"}

@app.get("/patientHome")
def home():
    # Retorna uma mensagem simples como resposta quando o endpoint "/" for acessado.
    return {"message": "Bem-vindo, {patient_name}}"}

"""
@app.post("/Login")
def login
"""