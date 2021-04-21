from uuid import uuid4
from functools import wraps
from requests import get
from flask import request
from api.restplus import api
from database.models import User, Joke


def gen_token():
    times = 15
    cur = 0

    token = None
    while cur < times:
        token = uuid4().hex
        user = User.query.filter(User.token == token).first()
        if user is None:
            return token

    api.abort(500, "Cannot create user, try again.")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if token is None:
            api.abort(401, "Token is missing.")

        user = User.query.filter(User.token == token).first()
        if user is None:
            api.abort(403, "Not Authorized.")

        return f(user, *args, **kwargs)

    return decorated


def get_last_joke_id(user):
   joke = Joke.query.filter(Joke.user == user).order_by(Joke.user_joke_id.desc()).first()
   if joke is not None:
       return joke.user_joke_id
   else:
       return 0

joke_url = "https://geek-jokes.sameerkumar.website/api"
def generate_joke():
    r = get(joke_url)
    return r.content.decode().strip().strip("\"")
