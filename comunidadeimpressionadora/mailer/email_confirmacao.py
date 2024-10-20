 # Funções para geração de código, token e envio de e-mail de confirmação

from flask_mail import Message
from flask import render_template, url_for
from comunidadeimpressionadora import mail
from .helpers import gerar_confirmar_url
import threading

def enviar_email_de_confirmacao(usuario):
    confirmar_url = gerar_confirmar_url(usuario)
    codigo_confirmacao = usuario.codigo_confirmacao
    html = render_template('confirmar_email.html', confirmar_url=confirmar_url, codigo_confirmacao=codigo_confirmacao)
    msg = Message('Confirme seu E-mail', sender='noreply@seusite.com', recipients=[usuario.email])
    msg.html = html
    thread = threading.Thread(target=enviar_email_thread, args=(msg,))
    thread.start()
