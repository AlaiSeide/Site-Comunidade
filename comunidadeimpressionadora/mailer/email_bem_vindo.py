# Funções relacionadas ao e-mail de boas-vindas

from flask_mail import Message
from flask import render_template, url_for
from comunidadeimpressionadora import mail

def enviar_email_de_boas_vindas(usuario):
    msg = Message('Bem-vindo à Comunidade!', recipients=[usuario.email])
    link = url_for('perfil', _external=True).replace("127.0.0.1:5000", "meusite.com")
    msg.html = render_template('email_bem_vindo.html', usuario=usuario, link=link)
    mail.send(msg)
