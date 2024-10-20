from flask_mail import Message
from flask import render_template
from threading import Thread
from .email_threading import enviar_email_thread

def enviar_email_exclusao_conta(usuario):
    """
    Envia um e-mail de notificação para o usuário informando sobre a exclusão de sua conta.

    Esta função gera uma mensagem de e-mail com o título 'Conta Excluída - Comunidade' e 
    usa um template HTML para personalizar o conteúdo da mensagem. O e-mail é enviado 
    utilizando Flask-Mail de forma assíncrona (em segundo plano) para evitar bloqueios no sistema.

    Parâmetros:
    usuario (objeto): Um objeto que contém os dados do usuário, incluindo o e-mail.

    Funcionalidade:
    - Verifica se o usuário tem um e-mail válido.
    - Renderiza o template HTML 'email_exclusao_conta.html' com as informações do usuário.
    - Cria a mensagem de e-mail e envia utilizando uma thread, para que o envio aconteça 
      em segundo plano, sem bloquear a aplicação.

    Exceções:
    - ValueError: Lançada se o usuário não tiver um e-mail válido.
    - Exception: Captura qualquer erro durante o envio do e-mail.

    Retorna:
    None

    Como Usar:
    -----------
    Para enviar um e-mail de exclusão de conta de forma segura e assíncrona, siga os passos abaixo:

    1. Importe a função `enviar_email_exclusao_conta`.
    2. Passe um objeto `usuario` com os dados do usuário, incluindo o e-mail.
    3. A função enviará o e-mail em segundo plano.

    Exemplo de Uso:

    ```python
    from comunidadeimpressionadora.threading import enviar_email_exclusao_conta

    # Chame a função com o objeto 'usuario' apropriado
    enviar_email_exclusao_conta(usuario)
    ```

    O envio do e-mail será realizado em segundo plano para garantir que a aplicação 
    continue funcionando normalmente enquanto o e-mail é enviado.
    """
    try:
        # Verifica se o usuário tem um e-mail válido
        if not usuario.email:
            raise ValueError("O usuário não tem um e-mail válido.")

        # Cria a mensagem de e-mail
        msg = Message(
            'Conta Excluída - Comunidade',          # Assunto do e-mail
            recipients=[usuario.email]              # Destinatário
        )
        
        # Renderiza o template HTML do e-mail com os dados do usuário
        msg.html = render_template('email/email_exclusao_conta.html', usuario=usuario)

        # Envia o e-mail em segundo plano usando threading
        Thread(target=enviar_email_thread, args=(msg,)).start()

    except Exception as e:
        # Captura qualquer erro e o exibe
        print(f"Erro ao enviar o e-mail de exclusão de conta: {e}")
