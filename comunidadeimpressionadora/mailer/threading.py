# Função para enviar e-mail em thread


from comunidadeimpressionadora import mail, app

def enviar_email_thread(msg):
    with app.app_context():
        mail.send(msg)
