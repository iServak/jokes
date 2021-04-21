import os
import logging
import logging.config
import settings
import click
from flask import Flask, Blueprint
from flask.cli import AppGroup, with_appcontext
from database import db, reset_database
from database.models import User
from api import users
from api.logs import create_log_entry
from api.restplus import api
from api.endpoints.users import ns as users_ns
from api.endpoints.jokes import ns as jokes_ns
from api.endpoints.logs import ns as logs_ns


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "./logging.conf"))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)



user_cli = AppGroup("user")
@user_cli.command("set-admin")
@click.argument("name")
@with_appcontext
def set_admin(name):
    init_app(app)
    user = User.query.filter(User.username == name).first()
    if user is None:
        print("Not found!")
        return
    users.set_admin(user)
    create_log_entry(type="users", description="{} promoted to admin".format(user), user=user, ip=None, datetime=datetime.now())
    log.warning("{} promoted to admin!".format(user))

app.cli.add_command(user_cli)

db_cli = AppGroup("db")
@db_cli.command("reset")
@with_appcontext
def db_reset():
    init_app(app)
    reset_database()
    log.warning("Database was reset successfully.")
app.cli.add_command(db_cli)


def init_app(flask_app):
    flask_app.config.from_object("settings")

    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    api.add_namespace(jokes_ns)
    api.add_namespace(logs_ns)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


if __name__ == "__main__":
    init_app(app)
    app.run(host="0.0.0.0")
