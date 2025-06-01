from sqlalchemy.orm import Session
from api.app.models.models import User
from typing import List

def get_all_patients(db: Session) -> List[dict]:
    patients = db.query(User).filter(User.user_type == 'patient').all()
    return [{"id": p.id, "name": f"{p.first_name} {p.last_name}"} for p in patients]