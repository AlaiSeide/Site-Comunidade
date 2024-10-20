# Funções auxiliares, como geração de tokens e códigos


import random
import string
from itsdangerous import URLSafeTimedSerializer
from comunidadeimpressionadora import app

def gerar_codigo_confirmacao():
    return ''.join(random.choices(string.digits, k=6))

def gerar_token_seguranca(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation-salt')

def validar_token_confirmacao_email(token, expiracao=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=expiracao)
    except:
        return False
    return email

def gerar_confirmar_url(usuario):
    token = gerar_token(usuario.email)
    confirmar_url = url_for('confirmar_email', token=token, _external=True, _scheme='http')
    confirmar_url = confirmar_url.replace('localhost', '192.168.220.112')
    return confirmar_url
