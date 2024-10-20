 # Funções para geração de código, token e envio de e-mail de confirmação

from flask_mail import Message
from flask import render_template, url_for
from .helpers import gerar_confirmar_url
from .email_threading import enviar_email_thread
from threading import Thread

def enviar_email_de_confirmacao(usuario):
    """
    Envia um e-mail de confirmação de conta para o usuário.

    Esta função gera uma URL de confirmação e um código de confirmação, renderiza um template HTML
    para o e-mail de confirmação e o envia em segundo plano utilizando uma thread para evitar atrasos
    na resposta da aplicação.

    Parâmetros:
    usuario (objeto): Um objeto que contém os dados do usuário, incluindo o e-mail e o código de confirmação.

    Funcionalidade:
    - Gera a URL de confirmação usando a função `gerar_confirmar_url()`.
    - Pega o código de confirmação do usuário.
    - Renderiza o template de e-mail 'confirmar_email.html' passando o link e o código de confirmação.
    - Cria uma mensagem de e-mail com o remetente 'noreply@seusite.com' e o destinatário sendo o e-mail do usuário.
    - Inicia uma thread para enviar o e-mail sem bloquear a execução do programa principal.
    
    Exceções:
    - ValueError: Lançada se o usuário não tem um e-mail válido.
    - Exception: Captura qualquer outro erro inesperado, exibindo uma mensagem de erro.

    Retorna:
    None
    """
    try:
        if not usuario.email:
            # Lança um erro se o e-mail do usuário não for válido e para a execucao
            raise ValueError("O usuário não tem um e-mail válido.")

        confirmar_url = gerar_confirmar_url(usuario)
        codigo_confirmacao = usuario.codigo_confirmacao

        html = render_template('email/confirmar_email.html', 
            confirmar_url=confirmar_url, 
            codigo_confirmacao=codigo_confirmacao)

        msg = Message('Confirme seu E-mail', 
            sender='noreply@seusite.com', 
            recipients=[usuario.email])

        msg.html = html
        Thread(target=enviar_email_thread, args=(msg,)).start()

    except Exception as e:
        # Captura qualquer erro que possa acontecer
        print(f"Erro ao tentar enviar o e-mail de confirmação: {e}")
