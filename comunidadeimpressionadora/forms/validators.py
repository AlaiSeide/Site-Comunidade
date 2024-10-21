import re
from wtforms import ValidationError
from comunidadeimpressionadora.model import Usuario


def validar_senha(senha, username=None, email=None):
    """
    Valida a senha de acordo com os critérios de segurança.

    Parâmetros:
    senha (str): A senha que será validada.
    username (str, opcional): O nome de usuário, usado para evitar que seja incluído na senha.
    email (str, opcional): O e-mail do usuário, usado para evitar que partes do e-mail estejam na senha.

    Levanta:
    ValidationError: Se a senha não atender aos critérios de segurança.
    """
    # Verificar se a senha contém pelo menos uma letra minúscula, uma maiúscula, um número e um caractere especial
    if not re.search(r'[A-Z]', senha):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[a-z]', senha):
        raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
    if not re.search(r'[0-9]', senha):
        raise ValidationError('A senha deve conter pelo menos um número.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        raise ValidationError('A senha deve conter pelo menos um caractere especial (!@#$%^&* etc.).')

    # Proibir senhas muito comuns (exemplo simples, pode ser estendido)
    senhas_comuns = ['password', '123456', 'senha123', 'admin', '12345678']
    if senha.lower() in senhas_comuns:
        raise ValidationError('Esta senha é muito comum, escolha uma senha mais segura.')

    # Evitar que a senha contenha o nome de usuário ou partes do e-mail
    if username and username.lower() in senha.lower():
        raise ValidationError('A senha não deve conter seu nome de usuário.')
    if email and email.split('@')[0].lower() in senha.lower():
        raise ValidationError('A senha não deve conter partes do seu e-mail.')

def validar_email_unico(email):
    """
    Verifica se o e-mail já está registrado no banco de dados.

    Parâmetros:
    email (str): O e-mail a ser verificado.

    Levanta:
    ValidationError: Se o e-mail já estiver cadastrado no banco de dados, ou se a conta não foi confirmada.
    """
    usuario = Usuario.query.filter_by(email=email.data).first()

    if usuario:
        if not usuario.confirmado:
            raise ValidationError('Este e-mail já foi registrado, mas a conta não foi confirmada. Reenvie o e-mail de confirmação ou use outro e-mail.')
        else:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')

# Lista de domínios de e-mails temporários (você pode expandir essa lista)
dominios_temporarios = ['mailinator.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com']

def validar_email_temporario(email):
    """
    Verifica se o e-mail pertence a um serviço de e-mail temporário.

    Parâmetros:
    email (str): O e-mail que será verificado.

    Levanta:
    ValidationError: Se o e-mail for de um domínio temporário.
    """
    dominio = email.data.split('@')[1]  # Extrai o domínio do e-mail
    if dominio in dominios_temporarios:
        raise ValidationError('E-mails de domínios temporários não são permitidos. Use um e-mail válido.')

import dns.resolver

def validar_email_dns(email):
    """
    Verifica se o domínio do e-mail possui registros MX, indicando que pode receber e-mails.

    Parâmetros:
    email (str): O e-mail que será verificado.

    Levanta:
    ValidationError: Se o domínio do e-mail não possuir registros MX válidos.
    """
    dominio = email.data.split('@')[1]  # Extrai o domínio do e-mail

    try:
        # Verifica se o domínio tem um registro MX (Mail Exchange)
        dns.resolver.resolve(dominio, 'MX')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        raise ValidationError(f'O domínio {dominio} não pode receber e-mails.')
    except dns.exception.DNSException:
        raise ValidationError('Erro ao verificar o domínio. Tente novamente mais tarde.')
