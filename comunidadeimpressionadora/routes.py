from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEdiarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


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
@login_required
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
        # Então, resumindo, essa linha de código está procurando no banco de dados pelo usuário que possui o email fornecido no formulário de login e armazenando esse usuário na variável usuario.
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        #print(usuario.senha)
        # se o usuario existe e se a senha que ele preencheu é a mesma que ta no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # fazendo login do usuario
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # exibir msg de login feito com sucesso aseguido do e-amil dessa pessoal
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            # redirecionar para outra pagina
            # o return deve estar sempre atras do redirect(url_for('home'))

            # Obtém o parâmetro 'next' da query string da URL, que é geralmente usado para redirecionar o usuário após o login.
            parametro_next = request.args.get('next')
            # Verifica se o parâmetro 'next' foi fornecido na query string.
            if parametro_next:
                # Se o parâmetro 'next' estiver presente, redireciona o usuário para o URL fornecido pelo parâmetro 'next'.
                return redirect(parametro_next)
            else:
                # Se o parâmetro 'next' não estiver presente, redireciona o usuário para a página inicial ('home') da aplicação.
                return redirect(url_for("home"))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.','alert-danger')

            
    # Verifica se o usuario criou conta com sucesso
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #print(senha_cript)
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


# pagina de sair
@app.route('/sair')
@login_required
def sair():
    # sair e redirecionar para a pagina home
    logout_user()
    flash('Logout feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))

# pagina de ver o perfil
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

# pagina de criar post
@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    # uma instancia da minha classe FormEdiarPerfil
    formeditarperfil = FormEdiarPerfil()

    # validar o meu formulario
    if formeditarperfil.validate_on_submit():
        current_user.email = formeditarperfil.email.data
        current_user.username = formeditarperfil.username.data
        database.session.commit()
        flash(f'Perfil Atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    # preencher o formulario automaticamente
    # Verifica se a requisição HTTP é do tipo GET, ou seja, se é a primeira vez que a página está sendo carregada.
    elif request.method == 'GET':
        # Se a requisição for do tipo GET, preenche os campos do formulário de edição de perfil com os dados atuais do usuário.
        # Preenche o campo de e-mail com o e-mail atual do usuário logado.
        formeditarperfil.email.data = current_user.email
        # Preenche o campo de nome de usuário com o nome de usuário atual do usuário logado.
        formeditarperfil.username.data = current_user.username
    
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, formeditarperfil=formeditarperfil)