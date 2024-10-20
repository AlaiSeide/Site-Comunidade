from flask_mail import Message
from flask import render_template
from threading import Thread
from .email_threading import enviar_email_thread

def enviar_email_alteracao_senha(usuario):
    """
    Envia um e-mail notificando o usuário sobre a alteração de sua senha.

    Esta função gera uma mensagem de e-mail com o título 'Alteração de Senha - Comunidade'
    e utiliza um template HTML para personalizar o conteúdo da mensagem.
    O e-mail é enviado de forma assíncrona (em segundo plano) utilizando threading.

    Parâmetros:
    usuario (objeto): Um objeto que contém os dados do usuário, incluindo o e-mail.

    Funcionalidade:
    - Verifica se o usuário tem um e-mail válido.
    - Renderiza o template HTML 'email_alteracao_senha.html' com as informações do usuário.
    - Cria a mensagem de e-mail e a envia utilizando uma thread.

    Exceções:
    - ValueError: Lançada se o usuário não tiver um e-mail válido.
    - Exception: Captura qualquer erro durante o envio do e-mail.

    Retorna:
    None
    """
    try:
        # Verifica se o usuário tem um e-mail válido
        if not usuario.email:
            raise ValueError("O usuário não tem um e-mail válido.")
        
        # Cria a mensagem de e-mail
        msg = Message(
            'Alteração de Senha - Comunidade',      # Assunto do e-mail
            recipients=[usuario.email]              # Destinatário
        )

        # Renderiza o template HTML do e-mail com os dados do usuário
        msg.html = render_template('email/email_alteracao_senha.html', usuario=usuario)

        # Envia o e-mail em segundo plano usando threading
        Thread(target=enviar_email_thread, args=(msg,)).start()

    except Exception as e:
        print(f"Erro ao enviar o e-mail de alteração de senha: {e}")


def enviar_email_confirmacao_de_redefinicao_de_senha(usuario):
    """
    Envia um e-mail confirmando que a senha do usuário foi redefinida com sucesso.

    Esta função gera uma mensagem de e-mail com o título 'Sua senha foi redefinida com sucesso!'
    e utiliza um template HTML para personalizar o conteúdo da mensagem.
    O e-mail é enviado de forma assíncrona (em segundo plano) utilizando threading.

    Parâmetros:
    usuario (objeto): Um objeto que contém os dados do usuário, incluindo o e-mail.

    Funcionalidade:
    - Verifica se o usuário tem um e-mail válido.
    - Renderiza o template HTML 'email_confirmacao_redefinicao_senha.html' com as informações do usuário.
    - Cria a mensagem de e-mail e a envia utilizando uma thread.

    Exceções:
    - ValueError: Lançada se o usuário não tiver um e-mail válido.
    - Exception: Captura qualquer erro durante o envio do e-mail.

    Retorna:
    None
    """
    try:
        # Verifica se o usuário tem um e-mail válido
        if not usuario.email:
            raise ValueError("O usuário não tem um e-mail válido.")
        
        # Cria a mensagem de e-mail
        msg = Message(
            'Sua senha foi redefinida com sucesso!',  # Assunto do e-mail
            recipients=[usuario.email]                # Destinatário
        )

        # Renderiza o template HTML do e-mail com os dados do usuário
        msg.html = render_template('email/email_confirmacao_redefinicao_senha.html', usuario=usuario)

        # Envia o e-mail em segundo plano usando threading
        Thread(target=enviar_email_thread, args=(msg,)).start()

    except Exception as e:
        print(f"Erro ao enviar o e-mail de confirmação de redefinição de senha: {e}")
