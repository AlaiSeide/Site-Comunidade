from flask import render_template, redirect, url_for, flash, request, abort, session
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEdiarPerfil, ContatoForm, FormCriarPost, ConfirmarExclusaoContaForm, EsqueciSenhaForm, RedefinirSenhaForm, AlterarSenhaForm, ConfirmacaoEmailForm
from comunidadeimpressionadora.models import Usuario, Contato, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from functools import wraps
from PIL import Image
from comunidadeimpressionadora.forgotpassword import gerar_token, validar_token, enviar_email
from datetime import datetime, timezone
from comunidadeimpressionadora.utils import enviar_email_bem_vindo, enviar_email_alteracao_senha, enviar_email_exclusao_conta, enviar_email_confirmacao_redefinicao_senha, enviar_email_confirmacao, confirmar_token, gerar_codigo_confirmacao

# from flask_babel import gettext
# # No início de routes.py, após os imports
# print("Tipo de babel:", type(babel))
# print("Atributos do babel:", dir(babel))



# @babel.localeselector
# def get_locale():
#     return session.get('language', 'pt')

# # Rota para definir o idioma
# @app.route('/set_language/<language>')
# def set_language(language):
#     session['language'] = language
#     flash(gettext('Idioma alterado com sucesso!'), 'alert-success')
#     return redirect(request.referrer or url_for('perfil'))



##############
# Usuário diz que esqueceu a senha.
# Nós enviamos um link especial para o email dele.
# Ele clica no link e escolhe uma nova senha.
# Atualizamos a senha na nossa caixinha.

# Página para o usuário dizer que esqueceu a senha

# @app.route('/esqueci_senha', methods=['GET', 'POST'])
# def esqueci_senha():
#     if current_user.is_authenticated:
#         # Usuário já está logado, redirecionar para a página inicial ou perfil
#         return redirect(url_for('perfil'))  # Substitua 'inicio' pela rota adequada

#     if request.method == 'POST':
#         email = request.form['email']
#         # Aqui vamos procurar o usuário pelo email
#         usuario = Usuario.query.filter_by(email=email).first()
#         # se existir usuario
#         if usuario:
#             # Criar um token (chave especial)
#             token = gerar_token(usuario)
#             # Enviar o email com o link mágico
#             enviar_email(usuario.email, token)
#             flash('Um email foi enviado com instruções para redefinir sua senha.', 'alert-success')
#         else:
#             flash('Email não encontrado.', 'alert-info')
#         return redirect(url_for('login'))
#     return render_template('esqueci_senha.html')




# @app.route('/excluir_conta', methods=['GET', 'POST'])
# @login_required
# def excluir_conta():
#     form = DeleteAccountForm()
#     if form.validate_on_submit():
#         user = Usuario.query.get(current_user.id)
#         database.session.delete(user)
#         database.session.commit()
#         logout_user()
#         flash('Sua conta e todo o seu conteúdo foram excluídos.', 'alert-success')
#         return redirect(url_for('home'))
#     return render_template('excluir_conta.html', form=form)

# @app.route('/excluir_conta',  methods=['GET', 'POST'])
# @login_required
# def excluir_conta():
#     # Usamos o formulário com senha e checkbox de confirmação
#     delete_account_form = DeleteAccountForm()

#     if delete_account_form.validate_on_submit():
#         # Verificar se a senha fornecida está correta
#         if not bcrypt.check_password_hash(current_user.senha, delete_account_form.senha.data):
#             flash('Senha incorreta. Tente novamente.', 'alert-danger')
#             return redirect(url_for('excluir_conta'))
        
#         # Verificar se o checkbox foi marcado
#         if not delete_account_form.confirmacao.data:
#             flash('Você deve marcar a caixa de confirmação para excluir sua conta.', 'alert-danger')
#             return redirect(url_for('excluir_conta'))
        
#         # Se tudo estiver correto, proceder com a exclusão
#         usuario = Usuario.query.get(current_user.id)

#         # Enviar o e-mail de notificação de exclusão de conta
#         enviar_email_exclusao_conta(usuario)
        
#         # Excluir o usuário do banco de dados
#         database.session.delete(usuario)
#         database.session.commit()
        
#         # Fazer logout após excluir a conta
#         logout_user()
        
#         flash('Sua conta e todo o seu conteúdo foram excluídos.', 'alert-success')
#         return redirect(url_for('home'))  # Redirecionar para a página inicial
#     else:
#         # Se a requisição não for válida, mostrar uma mensagem de erro
#         flash('Requisição inválida.', 'alert-danger')
#         return redirect(url_for('perfil'))



