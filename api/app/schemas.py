# Importando BaseModel do Pydantic para validação de dados
from pydantic import BaseModel, EmailStr, \
    field_validator  # Importando classes do Pydantic para validação de dados e tipos específicos, como EmailStr
from datetime import time
from pydantic import BaseModel

# Esquema de criação de usuário com validação dos campos
class UsuarioCreate(
    BaseModel):  # Definindo o modelo Pydantic para criar um novo usuário. O Pydantic é usado para validar e serializar dados de entrada
    nome: str  # O campo 'nome' é uma string, representando o nome do usuário
    email: EmailStr  # O campo 'email' é validado automaticamente como um e-mail válido (EmailStr é um tipo específico do Pydantic)
    senha: str  # O campo 'senha' é uma string, representando a senha do usuário
    confirmacao_senha: str  # O campo 'confirmacao_senha' é uma string, representando a senha que o usuário deve confirmar
    aceitou_termos: bool  # O campo 'aceitou_termos' é um booleano, indicando se o usuário aceitou os termos de uso

    # Validador para garantir que a senha tenha no mínimo 6 caracteres
    @field_validator("senha")
    def validar_senha(cls, senha):  # Definindo um validador para o campo 'senha'
        if len(senha) < 6:  # Verifica se a senha tem pelo menos 6 caracteres
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")  # Lança uma exceção se a senha for curta
        return senha  # Retorna a senha validada

    # Validador para garantir que a senha e a confirmação de senha sejam iguais
    @field_validator("confirmacao_senha")
    def validar_confirmacao_senha(cls, confirmacao_senha,
                                  values):  # Definindo um validador para o campo 'confirmacao_senha'
        if "senha" in values and confirmacao_senha != values[
            "senha"]:  # Verifica se a senha e a confirmação de senha coincidem
            raise ValueError("As senhas não coincidem.")  # Lança uma exceção se as senhas não coincidirem
        return confirmacao_senha  # Retorna a confirmação de senha validada


# Esquema de resposta para exibir os dados do usuário
class UsuarioResponse(BaseModel):  # Definindo o modelo Pydantic para representar os dados do usuário na resposta da API
    id: int  # O campo 'id' é um número inteiro, representando o ID único do usuário
    nome: str  # O campo 'nome' é uma string, representando o nome do usuário
    is_admin: bool  # O campo 'is_admin' é um booleano, indicando se o usuário é administrador

    # Configuração para permitir que o Pydantic use atributos diretamente do modelo
    class Config:  # Definindo a configuração do Pydantic para mapear atributos diretamente do modelo do banco
        from_attributes = True  # Esta configuração permite que o Pydantic use os atributos diretamente do modelo SQLAlchemy sem precisar de um dicionário

# Esquema para criação de disponibilidade
class DisponibilidadeCreate(BaseModel):
    dia_semana: str  # Exemplo: 'segunda-feira'
    horario_inicio: time  # Exemplo: 09:00
    horario_fim: time  # Exemplo: 17:00


# Esquema de resposta de disponibilidade
class DisponibilidadeResponse(BaseModel):
    id: int
    dia_semana: str
    horario_inicio: time
    horario_fim: time
    psicologo_id: int

    class Config:
        from_attributes = True


class AgendamentoResponse(BaseModel):
    id: int
    paciente_id: int
    disponibilidade_id: int
    paciente_nome: str
    psicologo_id: int
    dia_semana: str
    horario_inicio: time
    horario_fim: time

    class Config:
        from_attributes = True