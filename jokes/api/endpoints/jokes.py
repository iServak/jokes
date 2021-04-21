import logging
from datetime import datetime
from flask import request
from flask_restplus import Resource
from api.restplus import api, authorizations
from api import serializers
from api import parsers
from api import jokes
from api.logs import create_log_entry
from api.utils import token_required, generate_joke
from database.models import Joke


log = logging.getLogger(__name__)


ns = api.namespace("jokes", description="Operations with jokes", security='apikey', authorizations = authorizations, decorators = [token_required])


@ns.route("/")
class JokeCollection(Resource):

    @api.expect(parsers.pagination_arguments)
    @api.marshal_with(serializers.page_of_jokes)
    def get(self, user):
        """
        Returns list of jokes.
        """
        args = parsers.pagination_arguments.parse_args(request)
        page = args.get("page", 1)
        per_page = args.get("per_page", 10)

        jokes_query = Joke.query.filter(Joke.user == user)
        joke_page = jokes_query.paginate(page, per_page, error_out=False)

        create_log_entry(type="jokes", description="{} requested list of jokes".format(user), user=user, ip=request.remote_addr, datetime=datetime.now())
        return joke_page


    @api.expect(serializers.create_joke, validate=True)
    @api.marshal_with(serializers.joke, skip_none=True)
    def post(self, user):
        """
        Creates a new joke.
        """
        joke = jokes.create(user, request.json)
        create_log_entry(type="jokes", description="{} created joke with id {}".format(user, joke.user_joke_id), user=user, ip=request.remote_addr, datetime=datetime.now())
        return joke, 201


@ns.route("/generate/")
class JokeGeneration(Resource):

    @api.marshal_with(serializers.joke, skip_none=True)
    def post(self, user):
        """
        Generates a joke.
        """
        joke_text = ""
        try:
            joke_text = generate_joke()
            if joke_text == "":
                raise
        except:
            create_log_entry(type="jokes", description="{} tried to create a joke with external API that was unavailable".format(user), user=user, ip=request.remote_addr, datetime=datetime.now())
            api.abort(503, "Service of generation jokes temporarily unavailable.")

        joke = jokes.create(user, {"text": joke_text})
        create_log_entry(type="jokes", description="{} created joke generated with external API with id {}".format(user, joke.user_joke_id), user=user, ip=request.remote_addr, datetime=datetime.now())
        return joke, 201


@ns.route("/<int:id>/")
@api.response(404, "Joke not found.")
class JokeEntry(Resource):

    @api.marshal_with(serializers.joke, skip_none=True)
    def get(self, user, id):
        """
        Returns a joke.
        """
        joke = Joke.query.filter(Joke.user_joke_id == id).filter(Joke.user == user).first()
        create_log_entry(type="jokes", description="{} requested joke with id {}".format(user, id), user=user, ip=request.remote_addr, datetime=datetime.now())
        if joke is None:
            return None, 404
        else:
            return joke


    @api.expect(serializers.joke, validate=True)
    @api.response(204, "Joke successfully updated.")
    def put(self, user, id):
        """
        Updates a joke.
        """
        text = request.json.get("text")
        joke = Joke.query.filter(Joke.user_joke_id == id).filter(Joke.user == user).first()
        if joke is None:
            create_log_entry(type="jokes", description="{} tried to update joke with id {}, but it doesn't exist".format(user, id), user=user, ip=request.remote_addr, datetime=datetime.now())
            return None, 404

        create_log_entry(type="jokes", description="{} updated joke with id {}".format(user, id), user=user, ip=request.remote_addr, datetime=datetime.now())
        joke = jokes.update(joke, text)
        return None, 204


    @api.response(204, "Joke successfully deleted.")
    def delete(self, user, id):
        """
        Deletes joke.
        """
        joke = Joke.query.filter(Joke.user_joke_id == id).filter(Joke.user == user).first()
        if joke is None:
            create_log_entry(type="jokes", description="{} tried to delete joke with id {}, but it doesn't exist".format(user, id), user=user, ip=request.remote_addr, datetime=datetime.now())
            return None, 404

        create_log_entry(type="jokes", description="{} deleted joke with id {}".format(user, id), user=user, ip=request.remote_addr, datetime=datetime.now())
        jokes.delete(joke)
        return None, 204
