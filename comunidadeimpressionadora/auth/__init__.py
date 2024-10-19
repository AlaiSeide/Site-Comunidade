from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from comunidadeimpressionadora.auth import routes
