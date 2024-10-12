# admin_views.py

from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request, abort
from comunidadeimpressionadora import admin, database, bcrypt
from comunidadeimpressionadora.models import Usuario, Post, Contato, TokenRedefinicao
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length

# Classe base para controlar o acesso ao painel administrativo
class AdminBaseView(ModelView):
    def is_accessible(self):
        # Permite acesso apenas a administradores autenticados
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redireciona para a página de login se o usuário não tiver acesso
        return redirect(url_for('login', next=request.url))

# Classe para gerenciar usuários
class UsuarioAdminView(AdminBaseView):
    column_list = ('username', 'email', 'is_admin')  # Colunas exibidas

    # Campos excluídos do formulário
    form_excluded_columns = ('senha', 'posts')

    # Campos adicionais no formulário de criação
    def create_form(self):
        form = super(UsuarioAdminView, self).create_form()
        form.senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
        return form

    # Processa os dados antes de salvar no banco
    def on_model_change(self, form, model, is_created):
        if is_created:
            # Criptografa a senha fornecida
            model.senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        else:
            # Mantém a senha atual ao editar
            existing_user = Usuario.query.get(model.id)
            model.senha = existing_user.senha

    # Impede a edição de usuários não administradores
    def edit_form(self, obj):
        form = super(UsuarioAdminView, self).edit_form(obj)
        if not obj.is_admin:
            for field_name, field in form._fields.items():
                field.render_kw = {'readonly': True}
        return form

# Classe para gerenciar posts
class PostAdminView(AdminBaseView):
    column_list = ('titulo', 'data_postagem', 'autor')

# Classe para gerenciar mensagens de contato
class ContatoAdminView(AdminBaseView):
    column_list = ('nome', 'email', 'assunto', 'data_envio')

# Classe para gerenciar tokens de redefinição
class TokenRedefinicaoAdminView(AdminBaseView):
    column_list = ('token', 'usuario_id', 'data_expiracao')

# Adiciona as visualizações ao painel administrativo
admin.add_view(UsuarioAdminView(Usuario, database.session, name='Usuários'))
admin.add_view(PostAdminView(Post, database.session, name='Posts'))
admin.add_view(ContatoAdminView(Contato, database.session, name='Mensagens de Contato'))
admin.add_view(TokenRedefinicaoAdminView(TokenRedefinicao, database.session, name='Tokens de Redefinição'))
