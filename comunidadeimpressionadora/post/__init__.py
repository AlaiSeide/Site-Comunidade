from flask import Blueprint

post_bp = Blueprint('post', __name__)

from comunidadeimpressionadora.post import routes
