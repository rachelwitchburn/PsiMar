# APP PSIMAR

Aplicação para atendimento psicológico com **FastAPI** no backend, **Flet** no frontend e **SQLAlchemy** para banco de dados.  
Este guia explica em detalhes como instalar e rodar tudo do zero.

---

## 🧰 PRÉ-REQUISITOS

Antes de tudo, você precisa:

1. **Instalar o [Python 3.10+](https://www.python.org/downloads/)**
   - Durante a instalação, **marque a opção "Add Python to PATH"**.
   - Após instalar, abra o terminal (Prompt de Comando ou PowerShell) e teste com:
     ```bash
     python --version
     ```
     Se aparecer algo como `Python 3.10.x`, está tudo certo!

2. **Instalar o [Visual Studio Code (VSCode)](https://code.visualstudio.com/)**
   - Após instalar, recomendamos instalar as extensões:
     - **Python**
     - **Pylance**
     - **Code Runner (opcional)**

3. **Instalar o Git (opcional, para baixar via repositório):**
   - [https://git-scm.com/downloads](https://git-scm.com/downloads)

---

## 📥 COMO BAIXAR O PROJETO

### 1° passo: Baixe o projeto na sua máquina

Você pode:
- **Baixar o ZIP** do repositório clicando em "Code > Download ZIP", ou
- **Clonar com Git** (opcional):
  ```bash
  git clone https://github.com/seu-usuario/seu-repositorio.git

  2° passo: Encontre o arquivo .zip na pasta de downloads
3° passo: Extraia o conteúdo do .zip

4° passo: Abra o projeto no VSCode
Clique em File > Open Folder e selecione a pasta extraída.

5° passo: Crie e ative um ambiente virtual
No terminal do VSCode (use Ctrl + `` para abrir), execute:
python -m venv venv

Depois, ative o ambiente virtual:

No Windows:
.\venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

📦 6° passo: Instalar as dependências
Dentro do ambiente virtual, rode:
pip install -r requirements.txt

<hr>
Como rodar o projeto:

Para atualizar o banco de dados:
alembic upgrade head

Para iniciar a API (backend):
uvicorn app.main:app --reload
A aplicação estará rodando em: http://127.0.0.1:8000
A documentação automática estará disponível em: http://127.0.0.1:8000/docs

🖥️ Frontend - Flet
Para rodar a interface gráfica com Flet, vá até a pasta do frontend (ex: frontend/) e execute:
python api.app.main.py



Sempre ative seu ambiente virtual antes de rodar comandos (.\venv\Scripts\activate).

Se der erro ao instalar algo, atualize o pip:
pip install --upgrade pip

Pode ser necessário instalar o Flet separadamente:
pip install flet
