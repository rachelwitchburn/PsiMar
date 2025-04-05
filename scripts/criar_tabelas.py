# criar_tabelas_sqlalchemy.py
from app.models import Base
from sqlalchemy import create_engine
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bd", "banco_de_dados.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

def criar_banco():
    Base.metadata.create_all(engine)
    print("Banco e tabelas criados com sucesso com SQLAlchemy.")

if __name__ == "__main__":
    criar_banco()
