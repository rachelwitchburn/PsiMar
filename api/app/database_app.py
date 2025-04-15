from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os

db_dir = 'build'
db_file = os.path.join(db_dir, 'database.sqlite')
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.sqlite")

if not os.path.exists('build'):
    os.makedirs('build')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

if not os.path.exists('sqlite:///./database.sqlite'):
    Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()  # Em caso de erro, realiza o rollback
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados") from e
    finally:
        db.close()  # Garante que a sessão seja fechada após o uso
