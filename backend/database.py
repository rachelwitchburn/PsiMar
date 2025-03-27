#Conexão com o banco
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Caminho do bd
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../bd/banco_de_dados.db") 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.conffig["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

