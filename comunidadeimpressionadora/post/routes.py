from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from comunidadeimpressionadora import database
from comunidadeimpressionadora.post import post_bp
from comunidadeimpressionadora.forms import FormCriarPost
from comunidadeimpressionadora.models import Post

@post_bp.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    # Lógica para criar posts
    pass

@post_bp.route('/post/<int:post_id>', methods=['GET'])
def exibir_post(post_id):
    # Lógica para exibir um post
    pass
