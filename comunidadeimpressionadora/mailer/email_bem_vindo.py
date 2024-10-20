# Funções relacionadas ao e-mail de boas-vindas
from flask_mail import Message
from flask import render_template, url_for, current_app

from .email_threading import enviar_email_thread
from threading import Thread


def enviar_email_de_boas_vindas(usuario):
    """
    Envia um e-mail de boas-vindas para o novo usuário.

    Esta função cria uma mensagem de boas-vindas com um link para o perfil do usuário
    e envia o e-mail utilizando Flask-Mail. O envio é feito de forma assíncrona para
    não bloquear a execução do sistema.

    Parâmetros:
    usuario (objeto): Um objeto que contém os dados do usuário, incluindo o e-mail.

    Retorna:
    None
    """
    try:
        # Verifica se o usuário tem um e-mail válido
        if not usuario.email:
            raise ValueError("O usuário não tem um e-mail válido.")

        # Gera o link para o perfil do usuário, usando o domínio configurado
        link = url_for('user.perfil', _external=True)
        domain = current_app.config.get('SITE_DOMAIN', 'localhost:5000')
        # Substitui o endereço local pelo domínio real do site para que o link funcione para todos
        link = link.replace("127.0.0.1:5000", domain)

        # Renderiza o conteúdo do e-mail de boas-vindas
        msg = Message('Bem-vindo à Comunidade!', recipients=[usuario.email])
        msg.html = render_template('email/email_bem_vindo.html', usuario=usuario, link=link)

        # Enviar o e-mail em segundo plano usando threading
        Thread(target=enviar_email_thread, args=(msg,)).start()
     

    except Exception as e:
        # Captura qualquer erro e o exibe
        print(f"Erro ao enviar o e-mail de boas-vindas: {e}")

