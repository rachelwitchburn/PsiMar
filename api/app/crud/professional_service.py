from sqlalchemy.orm import Session
from api.app.models.models import User
from typing import List

def get_all_professionals(db: Session) -> List[dict]:
    professionals = db.query(User).filter(User.user_type == 'professional').all()
    return [{"id": p.id, "name": f"{p.first_name} {p.last_name}"} for p in professionals]