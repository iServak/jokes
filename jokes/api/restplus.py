import logging
import traceback

import settings
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(version="1.0", title="The Joke REST API", security="apikey", authorizations=authorizations)


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception(message)

    if not settings.DEBUG:
        return {"message": message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """No results found in database"""
    log.warning(traceback.format_exc())
    return {"message": "A database result was required but was empty."}, 404
