from flask import Flask, render_template, url_for


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
    # meus_usuarios=lista_usuarios está dentro da minha funcao render_template() para poder ser mostrado dentro da minha pagina html
    return render_template('usuarios.html', meus_usuarios=lista_usuarios)


# pagina de login e criar_conta
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)