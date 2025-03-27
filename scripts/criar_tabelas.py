import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bd", "banco_de_dados.db")

def criar_tabelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,                       
        senha TEXT NOT NULL,         
        tipo_usuario TEXT CHECK(tipo_usuario IN ('paciente', 'psicologo')) NOT NULL         
    );
                         
    CREATE TABLE IF NOT EXISTS CodigosAcesso (
        codigo TEXT PRIMARY KEY UNIQUE,
        utilizado BOOLEAN DEFAULT FALSE
    ); 
                         
    CREATE TABLE IF NOT EXISTS Psicologo (
        id INTEGER PRIMARY KEY,
        codigoAcesso TEXT NOT NULL,
        FOREIGN KEY (id) REFERENCES Usuario (id),
        FOREIGN KEY (codigoAcesso) REFERENCES CodigosAcesso (codigo)                   
    );
                         
    CREATE TABLE IF NOT EXISTS Paciente (
        id INTEGER PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES Usuario(id)                     
    );
    """)

    conn.commit()
    conn.close()
    print("tabelas criadas")

if __name__ == "__main__":
    criar_tabelas()