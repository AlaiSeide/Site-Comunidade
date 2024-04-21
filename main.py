from flask import Flask, render_template, url_for
from forms import FormCriarConta, FormLogin


app = Flask(__name__)

lista_usuarios = ['Alai', 'Samir', 'Onur', 'Jan']

app.config['SECRET_KEY'] = '0842ad099743ac670a2b8a9ff48f7c31'

# pagina principal
@app.route("/")
def home():
    return render_template('home.html')

# pagina de contato
@app.route("/contato")
def contato():
    return render_template('contato.html')

# pagina de usuarios
@app.route("/usuarios")
def usuarios():
    # meus_usuarios=lista_usuarios está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html
    return render_template('usuarios.html', meus_usuarios=lista_usuarios)


# pagina de login e criar_conta
@app.route('/login')
def login():

    # instanciando o meu formulario de login
    form_login = FormLogin()


    # instanciando o meu formulario de criar_conta
    form_criarconta = FormCriarConta()

    # form_login=form_login, form_criarconta=form_criarconta está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)