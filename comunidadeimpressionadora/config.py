import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'seuemail@gmail.com'
    
    # Adicione uma variável para o domínio
    SITE_DOMAIN = os.getenv('SITE_DOMAIN') or 'localhost:5000'

    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:Flashreverso2020..@localhost/Comunidade')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
