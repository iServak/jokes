from database import db
from database.models import User


def register(data):
    username = data.get("username")
    token = data.get("token")
    is_admin = data.get("is_admin", False)

    user = User.query.filter(User.username == username).first()
    print(user)
    if user is None:
        user = User(username=username, token=token, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return user
    else:
        return None


def set_admin(user):
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
