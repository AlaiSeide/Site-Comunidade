# Arquivo de banco de dados
# para poder criar o banco de dados precisamos da instancia desse banco de dados que esta no main.py

from comunidadeimpressionadora import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

# encontrar o usuario apartir de um id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(120), nullable=False, unique=True)
    senha = database.Column(database.String(80), nullable=False)
    foto_perfil = database.Column(database.String(50), nullable=False, default='default.jpg')
    # esse backref='autor' é para depois na tabela Post eu poder descobrir o autor do post
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String(500), nullable=False, default='Nao Informado')

    # quantidade de post que o cara tem
    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(50), nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # Use datetime.now(timezone.utc) para criar um datetime consciente do fuso horário UTC
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # 'usuario.id' é a minha tabela de Usuario pegando o id
    id_usuario = database.Column(database.Integer,  database.ForeignKey('usuario.id'), nullable=False)



class Contato(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    mensagem = database.Column(database.Text, nullable=False)