from flask import Blueprint

blueprint = Blueprint(
    'api_v1_blueprint',
    __name__,
    url_prefix='/v1'
)
