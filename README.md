# APP PSIMAR

Aplicação para atendimento psicológico com **FastAPI** no backend, **Flet** no frontend e **SQLAlchemy** para banco de dados.  
Este guia explica em detalhes como instalar e rodar tudo do zero.

---

## 🧰 PRÉ-REQUISITOS

Antes de tudo, você precisa:

✅ 1. Instalando o Python
🔹 Passo 1.1 — Acesse o site oficial
Vá até o site oficial do Python: https://www.python.org/downloads/

🔹 Passo 1.2 — Faça o download
Clique no botão amarelo: Download Python 3.X.X (a versão mais recente recomendada será mostrada).

Aguarde o download do instalador.

🔹 Passo 1.3 — Execute o instalador
Abra o arquivo baixado

Marque a opção: Add Python 3.X to PATH

Clique em Install Now

Aguarde até o fim da instalação

Clique em Close quando finalizar

⚠️ Importante: Marcar a opção Add Python to PATH garante que o Python seja reconhecido pelo terminal.

🔹 Passo 1.4 — Verificar instalação
Abra o terminal (Prompt de Comando no Windows ou Terminal no macOS/Linux) e digite:
python --version

Você deverá ver algo como:
Python 3.X.X



2. **Instalar a IDE (Recomendamos o Pycharm)**
  🔹 Passo 2.1 — Acesse o site oficial
Vá para: https://www.jetbrains.com/pycharm/download

🔹 Passo 2.2 — Baixe a versão Community Edition (gratuita)
🔹 Passo 2.3 — Instale o PyCharm
Execute o instalador

Marque as opções recomendadas:

Create Desktop Shortcut

Add "Open Folder as Project"

Clique em Install

Finalize e abra o PyCharm



3. **Instalando o projeto**
   Baixe o projeto na sua máquina

Você pode:
- **Baixar o ZIP** do repositório clicando em "Code > Download ZIP"
- Encontre o arquivo .zip na pasta de downloads
- Extraia o conteúdo do .zip


4. **Abrir o projeto no Pycharm**
 Na tela inicial, clique em New Project

Em Location, escolha a pasta onde deseja salvar

Em Python Interpreter, clique em:

   Selecione "Add Interpreter"

   Escolha "System Interpreter"

   Localize o executável do Python (ex: C:\Users\SeuNome\caminho_do_projeto)

Clique em OK

Clique em Create

ou:

Abra a sua IDE de escolha (por exemplo, Visual Studio Code, PyCharm, etc.).
No menu da IDE, selecione a opção Abrir pasta ou Open Folder.
Navegue até a pasta do projeto descompactado e clique em Abrir.



5. Instalando o SQLAlchemy
🔹 Passo 5.1 — Abrir o terminal do PyCharm
Dentro do projeto, abra o terminal inferior (aba Terminal na parte inferior da IDE)

🔹 Passo 5.2 — Instalar o SQLAlchemy via pip
pip install SQLAlchemy

Você verá uma saída semelhante a:
Successfully installed SQLAlchemy-X.X.X


Dica: Você pode verificar se o pacote foi instalado com:
pip show SQLAlchemy

6. Baixando as dependências (requirements.txt)
   Temos duas dependências, rode os comandos abaixo um após a execução total do outro:

   Rode o comando:
   pip install -r api/requirements.txt

   Em seguida rode:
   pip install -r client/requirements.txt
   

Volte para a raíz do projeto:
exit

7. **Configurando a opção de run automático para backend com fastapi""

   No canto superior direito da IDE, ao lado esquerdo do ícone de _play_ Configure as opções de configuração:
   Selecione 'Edit configurations'
   Aperte no ícone de + (mais) no canto superior esquerdo
   Adicione nova configuração
   Selecione FASTApi
   Insira o caminho para a api (backend)
   Aperte OK

8. Rodando o frontend
No terminal, rode o comando:

python api.app.main.py

Minimize.

9. Rodando o backend
   Rode a FASTApi manualmente pelo botão no canto superior direito que configuramos anteriormente.
   Ou
   Em outro terminal, rode:
   uvicorn app.main:app --reload


A aplicação estará rodando em: http://127.0.0.1:8000
A documentação automática estará disponível em: http://127.0.0.1:8000/docs



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
