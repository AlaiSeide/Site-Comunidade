# Funções relacionadas a e-mails de alteração e redefinição de senha

from flask_mail import Message
from flask import render_template
from comunidadeimpressionadora import mail

def enviar_email_alteracao_senha(usuario):
    msg = Message('Alteração de Senha - Comunidade', recipients=[usuario.email])
    msg.html = render_template('email_alteracao_senha.html', usuario=usuario)
    mail.send(msg)

def enviar_email_confirmacao_de_redefinicao_de_senha(usuario):
    msg = Message('Sua senha foi redefinida com sucesso!', recipients=[usuario.email])
    msg.html = render_template('email_confirmacao_redefinicao_senha.html', usuario=usuario)
    mail.send(msg)
