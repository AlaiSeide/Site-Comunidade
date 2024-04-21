from flask import Flask, render_template


app = Flask(__name__)

lista_usuarios = ['Alai', 'Samir', 'Onur', 'Jan']

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
    return render_template('usuarios.html', meus_usuarios=lista_usuarios)




if __name__ == '__main__':
    app.run(debug=True)