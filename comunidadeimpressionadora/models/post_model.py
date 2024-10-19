from comunidadeimpressionadora.extensions import database
from comunidadeimpressionadora.models import Usuario
from datetime import datetime, timezone


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(50), nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # Use datetime.now(timezone.utc) para criar um datetime consciente do fuso horário UTC
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # 'usuario.id' é a minha tabela de Usuario pegando o id
    id_usuario = database.Column(database.Integer,  database.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.id} de Usuário {self.id_usuario}>'
