from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = '0842ad099743ac670a2b8a9ff48f7c31'
# Configuração da URI do banco de dados SQLite
# Indica ao SQLAlchemy onde encontrar o banco de dados
# 'sqlite:///comunidade.db' significa que o banco de dados SQLite está localizado no arquivo 'comunidade.db' no diretório atual
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

# Criação de um objeto SQLAlchemy e associação à instância do Flask (app)
# SQLAlchemy é uma biblioteca para trabalhar com bancos de dados relacionais de forma orientada a objetos
# Associar o objeto SQLAlchemy à instância do Flask permite usar recursos do SQLAlchemy na aplicação Flask
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# a pagina onde o usuario sera redirecionado caso tente acessar uma pagina sem fazer login
# passei login que é a minha pagina de cadastro
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página, por favor.'
login_manager.login_message_category = 'alert-info'

# preciso executar o arquivo routes por isso importei ele aqui
from comunidadeimpressionadora import routes