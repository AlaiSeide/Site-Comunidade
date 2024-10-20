# Função de e-mail para exclusão de conta

from flask_mail import Message
from flask import render_template
from comunidadeimpressionadora import mail

def enviar_email_exclusao_conta(usuario):
    msg = Message('Conta Excluída - Comunidade', recipients=[usuario.email])
    msg.html = render_template('email_exclusao_conta.html', usuario=usuario)
    mail.send(msg)
