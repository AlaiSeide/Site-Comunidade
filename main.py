from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormCriarConta, FormLogin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

lista_usuarios = ['Alai', 'Samir', 'Onur', 'Jan']

app.config['SECRET_KEY'] = '0842ad099743ac670a2b8a9ff48f7c31'
# Configuração da URI do banco de dados SQLite
# Indica ao SQLAlchemy onde encontrar o banco de dados
# 'sqlite:///comunidade.db' significa que o banco de dados SQLite está localizado no arquivo 'comunidade.db' no diretório atual
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

# Criação de um objeto SQLAlchemy e associação à instância do Flask (app)
# SQLAlchemy é uma biblioteca para trabalhar com bancos de dados relacionais de forma orientada a objetos
# Associar o objeto SQLAlchemy à instância do Flask permite usar recursos do SQLAlchemy na aplicação Flask
database = SQLAlchemy(app)


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
# A funcao e uma pagina de formulario tem que ter o metodo POST/GET
@app.route('/login', methods=['GET', 'POST'])
def login():

    # instanciando o meu formulario de login a minha classe FormLogin()
    form_login = FormLogin()

    # instanciando o meu formulario de criar_conta a minha classe FormCriarConta()
    form_criarconta = FormCriarConta()

    # Verifica se o usuario fez login com sucesso
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # exibir msg de login feito com sucesso aseguido do e-amil dessa pessoal
        flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
        # redirecionar para outra pagina
        # o return deve estar sempre atras do redirect(url_for('home'))
        return redirect(url_for("home"))

    # Verifica se o usuario criou conta com sucesso
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # exibir msg de conta criada com sucesso
        flash(f'Conta Criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        # redirecionar para outra pagina
        # o return deve estar sempre atras do redirect(url_for('home'))
        return redirect(url_for("home"))

    # form_login=form_login, form_criarconta=form_criarconta está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)