from flask_restplus import reqparse


pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument("page", type=int, required=False, default=1, help="Page number")
pagination_arguments.add_argument("per_page", type=int, required=False, choices=[10, 25, 50, 100, 200], default=50, help="Results per page")
