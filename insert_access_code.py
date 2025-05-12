from sqlalchemy.orm import Session
from api.app.database_app import SessionLocal
from api.app.models.models import AccessCode

def inserir_codigo(code: str):
    db: Session = SessionLocal()
    novo_codigo = AccessCode(code=code, used=False)
    db.add(novo_codigo)
    db.commit()
    print(f"Código de acesso '{code}' inserido com sucesso.")
    db.close()

if __name__ == "__main__":
    inserir_codigo("codigo111")