import pyotp
import qrcode
from io import BytesIO
from flask import send_file

# Função para gerar uma chave secreta para o usuário
def gerar_chave_secreta():
    """
    Gera uma chave secreta aleatória para o usuário, que será usada para gerar códigos TOTP.
    
    Retorna:
        str: Uma chave secreta de base32.
    """
    return pyotp.random_base32()

# Função para gerar o URI do QR Code (usado para aplicativos como Google Authenticator)
def gerar_qr_code_uri(email, secret):
    """
    Gera o URI necessário para configurar o Google Authenticator no dispositivo do usuário.
    
    Parâmetros:
        email (str): O e-mail do usuário, usado para identificação no aplicativo 2FA.
        secret (str): A chave secreta gerada para o usuário.
    
    Retorna:
        str: O URI para ser usado na geração do QR Code.
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(email, issuer_name="SeuSite")

# Função para gerar e exibir o QR Code para o usuário
def exibir_qr_code(email, secret):
    """
    Gera e retorna um QR Code com o URI que o usuário deve escanear no Google Authenticator.
    
    Parâmetros:
        email (str): O e-mail do usuário.
        secret (str): A chave secreta gerada para o usuário.
    
    Retorna:
        Response: Uma resposta HTTP que contém o QR Code gerado.
    """
    uri = gerar_qr_code_uri(email, secret)
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Função para verificar o código 2FA fornecido pelo usuário
def verificar_codigo_2fa(secret, codigo_usuario):
    """
    Verifica se o código fornecido pelo usuário corresponde ao código gerado com a chave secreta.

    Parâmetros:
        secret (str): A chave secreta do usuário.
        codigo_usuario (str): O código de 6 dígitos fornecido pelo usuário.

    Retorna:
        bool: Retorna True se o código for válido, caso contrário False.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(codigo_usuario)
