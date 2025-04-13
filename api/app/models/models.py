import enum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, DECIMAL, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserTypeEnum(enum.Enum):
    patient = 'patient'
    professional = 'professional'


class AppointmentStatusEnum(enum.Enum):
    requested = 'requested'
    confirmed = 'confirmed'
    canceled = 'canceled'
    completed = 'completed'


class TaskStatusEnum(enum.Enum):
    pending = 'pending'
    completed = 'completed'


class PaymentMethodEnum(enum.Enum):
    card = 'card'
    transfer = 'transfer'
    cash = 'cash'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)

    patient = relationship("Patient", back_populates="user", uselist=False)
    professional = relationship("Professional", back_populates="user", uselist=False)


class AccessCode(Base):
    __tablename__ = 'access_code'

    code = Column(String, primary_key=True, unique=True)
    email = Column(String, nullable=False)
    used = Column(Boolean, default=False)


class Professional(Base):
    __tablename__ = 'professional'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    access_code = Column(String, ForeignKey('access_code.code'), nullable=False)

    user = relationship("User", back_populates="professional")
    patients = relationship("Patient", back_populates="professional")
    appointments = relationship("Appointment", back_populates="professional")
    schedule = relationship("Schedule", back_populates="professional")
    tasks = relationship("Task", back_populates="professional")
    feedbacks = relationship("Feedback", back_populates="professional")
    payments = relationship("Payment", back_populates="professional")


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    professional_id = Column(Integer, ForeignKey('professional.id'), nullable=False)

    user = relationship("User", back_populates="patient")
    professional = relationship("Professional", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    schedule = relationship("Schedule", back_populates="patient")
    tasks = relationship("Task", back_populates="patient")
    feedbacks = relationship("Feedback", back_populates="patient")
    payments = relationship("Payment", back_populates="patient")


class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatusEnum), default=AppointmentStatusEnum.requested)
    professional_id = Column(Integer, ForeignKey('professional.id'))
    patient_id = Column(Integer, ForeignKey('patient.id'))

    professional = relationship("Professional", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    payment = relationship("Payment", back_populates="appointment", uselist=False)


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    professional_id = Column(Integer, ForeignKey('professional.id'), nullable=False)
    date_time = Column(DateTime, nullable=False, unique=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))

    professional = relationship("Professional", back_populates="schedule")
    patient = relationship("Patient", back_populates="schedule")


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    professional_id = Column(Integer, ForeignKey('professional.id'))
    date = Column(DateTime)
    message = Column(Text)

    patient = relationship("Patient", back_populates="feedbacks")
    professional = relationship("Professional", back_populates="feedbacks")


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    professional_id = Column(Integer, ForeignKey('professional.id'))
    description = Column(Text, nullable=False)
    created_at = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.pending)

    patient = relationship("Patient", back_populates="tasks")
    professional = relationship("Professional", back_populates="tasks")


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    patient_id = Column(Integer, ForeignKey('patient.id'))
    professional_id = Column(Integer, ForeignKey('professional.id'))
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.pending)
    payment_method = Column(Enum(PaymentMethodEnum))

    appointment = relationship("Appointment", back_populates="payment")
    patient = relationship("Patient", back_populates="payments")
    professional = relationship("Professional", back_populates="payments")


class LoginAttempt(Base):
    __tablename__ = "login_attempt"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    failed_attempts = Column(Integer, default=0)
    lock_until = Column(DateTime, nullable=True)
    last_attempt = Column(DateTime, default=func.now())

    user = relationship("User")
