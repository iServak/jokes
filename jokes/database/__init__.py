from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from database.models import ActionType
    db.drop_all()
    db.create_all()
    db.session.add(ActionType(name="users"))
    db.session.add(ActionType(name="jokes"))
    db.session.commit()
