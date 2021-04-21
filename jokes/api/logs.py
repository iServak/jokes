from database import db
from database.models import ActionLog, ActionType


def create_log_entry(type, description, user, ip, datetime):
    action_type = ActionType.query.filter(ActionType.name == type).first()
    log_entry = ActionLog(type=action_type, user=user, ip=ip, description=description, datetime=datetime)
    db.session.add(log_entry)
    db.session.commit()
