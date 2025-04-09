import enum

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, DECIMAL
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TipoUsuarioEnum(enum.Enum):
    paciente = 'paciente'
    psicologo = 'psicologo'


class StatusConsultaEnum(enum.Enum):
    solicitada = 'solicitada'
    confirmada = 'confirmada'
    cancelada = 'cancelada'
    concluida = 'concluída'


class StatusTarefaEnum(enum.Enum):
    pendente = 'pendente'
    concluida = 'concluída'


class MetodoPagamentoEnum(enum.Enum):
    cartao = 'cartão'
    transferencia = 'transferencia'
    dinheiro = 'dinheiro'


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    tipo_usuario = Column(Enum(TipoUsuarioEnum), nullable=False)

    paciente = relationship("Paciente", back_populates="usuario", uselist=False)
    psicologo = relationship("Psicologo", back_populates="usuario", uselist=False)


class CodigoAcesso(Base):
    __tablename__ = 'codigos_acesso'

    codigo = Column(String, primary_key=True, unique=True)
    utilizado = Column(Boolean, default=False)


class Psicologo(Base):
    __tablename__ = 'psicologo'

    id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    codigoAcesso = Column(String, ForeignKey('codigos_acesso.codigo'), nullable=False)

    usuario = relationship("Usuario", back_populates="psicologo")
    pacientes = relationship("Paciente", back_populates="psicologo")
    consultas = relationship("Consulta", back_populates="psicologo")
    agenda = relationship("Agenda", back_populates="psicologo")
    tarefas = relationship("Tarefa", back_populates="psicologo")
    feedbacks = relationship("Feedback", back_populates="psicologo")
    pagamentos = relationship("Pagamento", back_populates="psicologo")


class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="paciente")
    psicologo = relationship("Psicologo", back_populates="pacientes")
    consultas = relationship("Consulta", back_populates="paciente")
    agenda = relationship("Agenda", back_populates="paciente")
    tarefas = relationship("Tarefa", back_populates="paciente")
    feedbacks = relationship("Feedback", back_populates="paciente")
    pagamentos = relationship("Pagamento", back_populates="paciente")


class Consulta(Base):
    __tablename__ = 'consulta'

    id = Column(Integer, primary_key=True)
    data_horario = Column(DateTime, nullable=False)
    status = Column(Enum(StatusConsultaEnum), default=StatusConsultaEnum.solicitada)
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'))
    paciente_id = Column(Integer, ForeignKey('paciente.id'))

    psicologo = relationship("Psicologo", back_populates="consultas")
    paciente = relationship("Paciente", back_populates="consultas")
    pagamento = relationship("Pagamento", back_populates="consulta", uselist=False)


class Agenda(Base):
    __tablename__ = 'agenda'

    id = Column(Integer, primary_key=True, autoincrement=True)
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'), nullable=False)
    data_horario = Column(DateTime, nullable=False, unique=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))

    psicologo = relationship("Psicologo", back_populates="agenda")
    paciente = relationship("Paciente", back_populates="agenda")


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'))
    data = Column(DateTime)
    mensagem = Column(Text)

    paciente = relationship("Paciente", back_populates="feedbacks")
    psicologo = relationship("Psicologo", back_populates="feedbacks")


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'))
    descricao = Column(Text, nullable=False)
    data_criacao = Column(DateTime)
    data_limite = Column(DateTime)
    status = Column(Enum(StatusTarefaEnum), default=StatusTarefaEnum.pendente)

    paciente = relationship("Paciente", back_populates="tarefas")
    psicologo = relationship("Psicologo", back_populates="tarefas")


class Pagamento(Base):
    __tablename__ = 'pagamento'

    id = Column(Integer, primary_key=True)
    consulta_id = Column(Integer, ForeignKey('consulta.id'))
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    psicologo_id = Column(Integer, ForeignKey('psicologo.id'))
    valor = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(StatusTarefaEnum), default=StatusTarefaEnum.pendente)
    metodo_pagamento = Column(Enum(MetodoPagamentoEnum))

    consulta = relationship("Consulta", back_populates="pagamento")
    paciente = relationship("Paciente", back_populates="pagamentos")
    psicologo = relationship("Psicologo", back_populates="pagamentos")


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True,
                index=True)
    user_id = Column(Integer,
                     index=True)
    failed_attempts = Column(Integer,
                             default=0)

    lock_until = Column(DateTime,
                        nullable=True)
