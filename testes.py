from main import app, database
from models import Usuario, Post


# with app.app_context():
#     database.create_all()

################################
# with app.app_context():
#     usuario = Usuario(
#         username='Alai',
#         email='tenw313@gmail.com',
#         senha='12345'
#     )

#     usuario2 = Usuario(
#         username='Maincon',
#         email='alaiseide2002@gmail.com',
#         senha='1111111'
#     )
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.commit()

# pegando informacoes do meu banco de dados

# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#     primeiro_usuario = meus_usuarios[0]
#     print(primeiro_usuario.posts)
#     segundo_usuario = meus_usuarios[1]
#     print(segundo_usuario.email)

with app.app_context():
    usuario_teste = Usuario.query.filter_by(id=2).first()
    print(usuario_teste)
    print(usuario_teste.username)