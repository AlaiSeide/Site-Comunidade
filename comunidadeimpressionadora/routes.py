from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user

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
        # criar usuario
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # se o usuario existe e se a senha que ele preencheu é a mesma que ta no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # fazendo login
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # exibir msg de login feito com sucesso aseguido do e-amil dessa pessoal
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            # redirecionar para outra pagina
            # o return deve estar sempre atras do redirect(url_for('home'))
            return redirect(url_for("home"))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.','alert-danger')

            
    # Verifica se o usuario criou conta com sucesso
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        # Criar o usuario
        # adicionar na sessao
        # dar commit da sessao
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        # exibir msg de conta criada com sucesso
        flash(f'Conta Criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        # redirecionar para outra pagina
        # o return deve estar sempre atras do redirect(url_for('home'))
        return redirect(url_for("home"))

    # form_login=form_login, form_criarconta=form_criarconta está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)
