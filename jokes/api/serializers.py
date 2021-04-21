from flask_restplus import fields
from api.restplus import api


register_user = api.model("User", {
    "username": fields.String(required=True, description="Username should be unique"),
})


pagination = api.model("A page of results", {
    "page": fields.Integer(description="Number of this page of results"),
    "pages": fields.Integer(description="Total number of pages of results"),
    "per_page": fields.Integer(description="Number of items per page of results"),
    "total": fields.Integer(description="Total number of results"),
})


joke = api.model("Joke", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a joke", attribute="user_joke_id"),
    "text": fields.String(required=True, description="Text of a joke"),
})


page_of_jokes = api.inherit("Page of jokes", pagination, {
    "items": fields.List(fields.Nested(joke))
})


create_joke = api.model("Joke", {
    "text": fields.String(required=True, description="Text of a joke"),
})


log = api.model("ActionLog", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a log entry"),
    "type": fields.String(required=True, description="Type of action"),
    "description": fields.String(required=True, description="Text of a joke"),
    "user": fields.String(required=True, description="User"),
    "ip": fields.String(required=True, description="Source IP"),
    "datetime": fields.String(required=True, description="Datetime"),
})

page_of_logs = api.inherit("Page of logs", pagination, {
    "items": fields.List(fields.Nested(log))
})
