from fastapi import FastAPI, Depends
from api.app.models.models import User
from api.app.security import get_current_user
from api.app.routers import users_router, auth_router, schedule_router, professional_router, patient_router, appointment_router, task_router, feedback_router, payment_router

# Criação da aplicação FastAPI com título personalizado
app = FastAPI(title="PSIMAR - Atendimento Psicológico")


# Aqui estamos incluindo os routers que serão responsáveis pelas rotas da API.
app.include_router(appointment_router.router)
app.include_router(auth_router.router)
app.include_router(patient_router.router)
app.include_router(professional_router.router)
app.include_router(schedule_router.router)
app.include_router(users_router.router)
app.include_router(task_router.router)
app.include_router(feedback_router.router)
app.include_router(payment_router.router)




# Rota inicial para testar o funcionamento da API
@app.get("/")
def root():
    return {"message": "API PSIMAR está rodando!"}
# Definindo uma rota simples para verificar se a API está funcionando corretamente.
@app.get("/professionalHome")
async def professional_home(current_user: User = Depends(get_current_user)):
    return {"message": f"Bem-vindo, {current_user.first_name}"}

@app.get("/patientHome")
async def patient_home(current_user: User = Depends(get_current_user)):
    return {"message": f"Bem-vindo, {current_user.first_name}"}





