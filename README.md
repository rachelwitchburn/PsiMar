# APP PSIMAR
Aplicação para atendimento psicológico com FastAPI.

✅ Como instalar dependências:

pip install -r api/requirements.txt
pip install -r client/requirements.txt

✅ Como rodar a API:

uvicorn api.app.main:app --reload

✅ Como testar a API (com pytest):

pytest
pytest tests/api --db-reset (para resetar o db após algum teste)

✅ Como iniciar banco de dados:

alembic upgrade head

✅ Endpoints principais (/docs com Swagger)

http://127.0.0.1:8000/docs