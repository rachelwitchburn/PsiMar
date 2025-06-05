from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.app.models.models import User, Professional, LoginAttempt, UserTypeEnum



MAX_ATTEMPTS = 5
LOCK_DURATION_MINUTES = 15

def authenticate_professional(access_code: str, db: Session):
    """
    Verifica as tentativas de login e autentica o profissional.
    Se o login falhar várias vezes, bloqueia o usuário temporariamente.
    """
    professional_user = (
        db.query(User)
        .join(Professional)
        .filter(
            Professional.access_code == access_code,
            User.user_type == UserTypeEnum.professional
        )
        .first()
    )

    professional_instance = (
        db.query(Professional)
        .filter(Professional.access_code == access_code)
        .first()
    )

    if not professional_instance:
        raise HTTPException(status_code=401, detail="Código de acesso inválido")

    user_id = getattr(professional_instance, 'id', None)  # ID do usuário profissional

    # Verifica as tentativas de login
    attempt = db.query(LoginAttempt).filter_by(user_id=user_id).first()
    now = datetime.now(timezone.utc)

    # Se o usuário estiver temporariamente bloqueado
    if attempt and attempt.lock_until and attempt.lock_until > now:
        raise HTTPException(
            status_code=403,
            detail=f"Tentativas excedidas. Tente novamente após {attempt.lock_until.strftime('%H:%M:%S')}."
        )

    # Se a autenticação falhar
    if not professional_user:
        if not attempt:
            attempt = LoginAttempt(user_id=user_id, failed_attempts=1, last_attempt=now)
            db.add(attempt)
        else:
            attempt.failed_attempts += 1
            attempt.last_attempt = now
            if attempt.failed_attempts >= MAX_ATTEMPTS:
                attempt.lock_until = now + timedelta(minutes=LOCK_DURATION_MINUTES)

        db.commit()
        raise HTTPException(status_code=401, detail="Código de acesso inválido")

    # Se a autenticação for bem-sucedida, resetar as tentativas
    if attempt:
        attempt.failed_attempts = 0
        attempt.lock_until = None
        attempt.last_attempt = now
        db.commit()

    return professional_user


