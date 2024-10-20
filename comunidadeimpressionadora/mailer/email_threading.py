from comunidadeimpressionadora.extensions import mail
from comunidadeimpressionadora import app

def enviar_email_thread(msg):
    """
    Envia um e-mail de forma assíncrona usando threading.

    Esta função permite que o envio de e-mails seja realizado em segundo plano, 
    sem bloquear o restante da aplicação. Ela utiliza o contexto da aplicação Flask 
    para garantir que todas as configurações necessárias estejam disponíveis.

    Parâmetros:
    msg (Message): Objeto de e-mail criado usando Flask-Mail, contendo o destinatário, 
    assunto e conteúdo do e-mail.

    Funcionalidade:
    - Utiliza o contexto da aplicação Flask para enviar o e-mail.
    - O envio é realizado de forma assíncrona, em segundo plano, utilizando threading.
    
    Exceções:
    - Garante que o e-mail seja enviado sem interferir na performance da aplicação,
      mas se ocorrerem erros durante o envio, eles precisam ser tratados em nível superior.

    Retorna:
    None

    Como Usar:
    -----------
    Para enviar um e-mail de forma assíncrona, siga os seguintes passos:

    1. Importe a função `enviar_email_thread` e a classe `Message` do Flask-Mail.
    2. Crie a mensagem de e-mail com remetente, destinatário e conteúdo (HTML ou texto simples).
    3. Inicie uma thread e passe a função `enviar_email_thread` como alvo, com a mensagem como argumento.

    Exemplo de Uso:

    ```python
    from flask_mail import Message
    from threading import Thread
    from comunidadeimpressionadora.threading import enviar_email_thread

    # Exemplo de criação de uma mensagem de e-mail
    msg = Message(
        'Assunto do E-mail',              # Assunto do e-mail
        sender='noreply@seusite.com',     # Remetente
        recipients=[usuario.email]        # Destinatário (e-mail do usuário)
    )

    # Conteúdo do e-mail em texto simples (opcional)
    msg.body = 'Olá, bem-vindo à nossa comunidade!'

    # Conteúdo do e-mail em HTML
    msg.html = '<p>Bem-vindo à nossa comunidade! Para mais informações, acesse o nosso site.</p>'

    # Enviar o e-mail em segundo plano usando threading
    Thread(target=enviar_email_thread, args=(msg,)).start()
    ```
    
    No exemplo acima:
    - O e-mail será enviado em segundo plano, sem bloquear a execução da aplicação.
    - `Thread(target=enviar_email_thread, args=(msg,)).start()` cria uma thread para enviar o e-mail de forma assíncrona.
    """
    with app.app_context():
        mail.send(msg)
