from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR, 'build')
db_file = os.path.join(db_dir, 'database.sqlite')

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_file}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

if not os.path.exists(db_file):
    Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        print(" ERRO NO BANCO:", str(e))  # Mostra no terminal
        raise HTTPException(status_code=500, detail=f"Erro real: {str(e)}")
    finally:
        db.close()

