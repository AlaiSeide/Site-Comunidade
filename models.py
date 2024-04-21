# Arquivo de banco de dados
# para poder criar o banco de dados precisamos da instancia desse banco de dados que esta no main.py

from main import database
from datetime import datetime

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Nao Informado')


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # Use datetime.now(timezone.utc) para criar um datetime consciente do fuso horário UTC
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer,  database.ForeignKey('usuario.id'), nullable=False)