from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from comunidadeimpressionadora import database, bcrypt
from comunidadeimpressionadora.user import user_bp
from comunidadeimpressionadora.forms import FormEdiarPerfil, AlterarSenhaForm
from comunidadeimpressionadora.models import Usuario

@user_bp.route('/perfil')
@login_required
def perfil():
    # Lógica de exibição de perfil aqui
    pass

@user_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    # Lógica de edição de perfil aqui
    pass

@user_bp.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    # Lógica de alteração de senha aqui
    pass
