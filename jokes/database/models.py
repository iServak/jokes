from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, username, token, is_admin=False):
        self.username = username
        self.token = token
        self.is_admin = is_admin


    def __repr__(self):
        return "<User {}>".format(self.username)


class Joke(db.Model):
    __tablename__ = "jokes"

    id = db.Column(db.Integer, primary_key=True)
    user_joke_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("jokes", lazy="dynamic"))


    def __init__(self, user, user_joke_id, text):
        self.user = user
        self.user_joke_id = user_joke_id
        self.text = text


    def __repr__(self):
        return "<Joke {} of user {}>".format(self.user_joke_id,  self.user.username)


db.Index("jokes_gix", db.metadata.tables["jokes"].c.user_joke_id, db.metadata.tables["jokes"].c.user_id, unique=True)


class ActionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)


    def __init(self, name):
        self.name = name


    def __repr__(self):
        return self.name


class ActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type_id = db.Column(db.Integer, db.ForeignKey("action_type.id"), nullable=False)
    type = db.relationship("ActionType", backref=db.backref("actionlog", lazy="dynamic"))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", backref=db.backref("actions", lazy="dynamic"))

    ip = db.Column(db.Text)
    description = db.Column(db.Text)
    datetime = db.Column(db.DateTime)


    def __init__(self, type, user, ip, description, datetime):
        self.type = type
        self.user = user
        self.ip = ip
        self.description = description
        self.datetime = datetime


    def __repr__(self):
        return "{} | {} | {}".format(self.datetime, self.user, self.description)
