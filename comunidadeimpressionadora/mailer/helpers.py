# Funções auxiliares, como geração de tokens e códigos


import random
import string
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from comunidadeimpressionadora import app
from flask import current_app, url_for

def gerar_codigo_confirmacao(tamanho=6):
    """
    Gera um código de confirmação de números aleatórios com um tamanho especificado.

    Parâmetros:
    tamanho (int): O tamanho do código de confirmação gerado (padrão é 6).

    Retorna:
    str: Um código de confirmação de 'tamanho' dígitos numéricos.

    Exemplo de Uso:
    ---------------
    codigo = gerar_codigo_confirmacao()
    print(codigo)  # Exemplo: 123456
    """
    return ''.join(random.choices(string.digits, k=tamanho))


def gerar_token_seguranca(email):
    """
    Gera um token de segurança com base no e-mail do usuário.

    Esta função utiliza o 'SECRET_KEY' da aplicação Flask para gerar um token seguro, 
    garantindo que o e-mail possa ser verificado de forma segura.

    Parâmetros:
    email (str): O e-mail do usuário para o qual o token será gerado.

    Retorna:
    str: Um token de segurança gerado para o e-mail.

    Exemplo de Uso:
    ---------------
    token = gerar_token_seguranca(usuario.email)
    print(token)  # Token de segurança gerado
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation-salt')


def validar_token_confirmacao_email(token, expiracao=3600):
    """
    Valida o token de confirmação de e-mail.

    Esta função verifica se o token gerado para a confirmação de e-mail é válido e
    se não expirou dentro do tempo especificado.

    Parâmetros:
    token (str): O token gerado para o e-mail de confirmação.
    expiracao (int, opcional): O tempo de expiração do token em segundos. O padrão é 3600 segundos (1 hora).

    Retorna:
    str | bool: O e-mail associado ao token se for válido, ou False se o token for inválido ou expirado.

    Exemplo de Uso:
    ---------------
    email = validar_token_confirmacao_email(token)
    if email:
        print("Token válido. E-mail:", email)
    else:
        print("Token inválido ou expirado.")
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=expiracao)
    except SignatureExpired:
        # Token expirou
        return False
    except BadSignature:
        # Token inválido
        return False
    return email


def gerar_confirmar_url(usuario):
    """
    Gera uma URL de confirmação de e-mail com base no token de segurança do usuário.

    Esta função cria uma URL de confirmação que o usuário pode acessar para verificar seu e-mail.
    O token gerado é utilizado para associar a URL ao usuário, garantindo a segurança do processo de verificação.

    Parâmetros:
    usuario (objeto): Um objeto que contém o e-mail do usuário.

    Retorna:
    str: A URL de confirmação gerada para o e-mail do usuário.

    Exemplo de Uso:
    ---------------
    confirmar_url = gerar_confirmar_url(usuario)
    print(confirmar_url)  # Exemplo: http://meusite.com/confirmar_email/<token>
    """
    token = gerar_token_seguranca(usuario.email)
    confirmar_url = url_for('auth.confirmar_email', token=token, _external=True, _scheme='http')

    # Substitui 'localhost' pelo domínio correto, configurável
    domain = current_app.config.get('SITE_DOMAIN', 'localhost:5000')
    confirmar_url = confirmar_url.replace('localhost', domain)
    
    return confirmar_url
