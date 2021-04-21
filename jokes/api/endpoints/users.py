import logging
from datetime import datetime
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api import serializers
from api import parsers
from api import users
from api.logs import create_log_entry
from database.models import User
from api.utils import gen_token


log = logging.getLogger(__name__)


ns = api.namespace('users', description='Operations with users')


@ns.route('/')
class UserRegistration(Resource):

    @api.doc(security=[])
    @api.expect(serializers.register_user, validate=True)
    def post(self):
        """
        Registers a new user.
        """
        username = request.json.get("username")
        token = gen_token()
        params = {"username": username, "token": token}
        res = users.register(params)
        if res is not None:
            create_log_entry(type="users", description="{} registered".format(res), user=res, ip=request.remote_addr, datetime=datetime.now())
            params["description"] = "Use token to work with API"
            return params, 201
        else:
            create_log_entry(type="users", description="User with name {} already exists".format(username), user=None, ip=request.remote_addr, datetime=datetime.now())
            return {"description": "User with this name already exists"}, 403
