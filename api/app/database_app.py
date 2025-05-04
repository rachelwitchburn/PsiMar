from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DATABASE_FILE = BASE_DIR / "build" / "database.sqlite"
DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)


DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
