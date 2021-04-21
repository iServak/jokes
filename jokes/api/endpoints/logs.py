import logging

from flask import request
from flask_restplus import Resource
from api.restplus import api, authorizations
from api import serializers
from api import parsers
from api import logs
from api.utils import token_required
from database.models import ActionLog, ActionType


log = logging.getLogger(__name__)


ns = api.namespace("logs", description="Operations with logs", security='apikey', authorizations = authorizations, decorators = [token_required])


@ns.route("/")
class LogCollection(Resource):

    @api.expect(parsers.pagination_arguments)
    @api.marshal_with(serializers.page_of_logs)
    def get(self, user):
        """
        Returns list of logs.
        """
        if not user.is_admin:
            api.abort(403, "Access denied.")

        args = parsers.pagination_arguments.parse_args(request)
        page = args.get("page", 1)
        per_page = args.get("per_page", 50)

        logs_query = ActionLog.query
        log_page = logs_query.paginate(page, per_page, error_out=False)

        return log_page
