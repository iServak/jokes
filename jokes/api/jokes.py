from database import db
from database.models import Joke
from api.utils import get_last_joke_id

def create(user, data):
    id = get_last_joke_id(user)
    text = data.get("text")
    joke = Joke(user=user, user_joke_id=id+1, text=text)
    db.session.add(joke)
    db.session.commit()
    return joke


def update(joke, text):
    joke.text = text
    db.session.add(joke)
    db.session.commit()
    return joke


def delete(joke):
    db.session.delete(joke)
    db.session.commit()
