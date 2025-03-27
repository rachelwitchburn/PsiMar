import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bd", "banco_de_dados.db")

def criar_bd():
    if os.path.exists(DB_PATH):
        print('Banco de dados já existe.')
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.close()
    print('Banco de dados criado com sucesso!!')

if __name__ == "__main__":
    criar_bd()