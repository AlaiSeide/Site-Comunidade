from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user


from comunidadeimpressionadora import bcrypt, database

from comunidadeimpressionadora.auth import auth_bp
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario


from comunidadeimpressionadora.utils import enviar_email_confirmacao, gerar_codigo_confirmacao

# pagina de login e criar_conta
# A funcao e uma pagina de formulario tem que ter o metodo POST/GET
@auth_bp.route('/login', methods=['GET', 'POST'])
def login(): 
    # se o usuario estiver autenticado redireciona para o home, impedir ele de acessar a pagina de login
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # instanciando o meu formulario de login a minha classe FormLogin()
    form_login = FormLogin()

    # instanciando o meu formulario de criar_conta a minha classe FormCriarConta()
    form_criarconta = FormCriarConta()
    # Verifica se o usuario fez login com sucesso
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # Então, resumindo, essa linha de código está procurando no banco de dados pelo usuário que possui o email fornecido no formulário de login e armazenando esse usuário na variável usuario.
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        #print(usuario.senha)
        # se o usuario existe e se a senha que ele preencheu é a mesma que ta no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # deixa o usuario fazer login se ele ja confirmou o seu email
            if usuario.confirmado:
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
                    return redirect(url_for("main.home"))
            else:
                flash(f'Por favor, confirme o seu e-mail para poder acessar sua conta e fazer login.','alert-info')
                return redirect(url_for("unconfirmed"))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.','alert-danger')

            
        """
        request.form é um dicionário que contém todos os campos do formulário. A chave é o nome do campo e o valor é o valor do campo. Então, 'botao_submit_criarconta' in request.form verifica se a chave 'botao_submit_criarconta' está presente no dicionário request.form, o que significaria que o botão de submit do formulário de criação de conta foi pressionado."""
   
    # Verifica se o usuario criou conta com sucesso
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Gera o código de confirmação
        codigo_confirmacao = gerar_codigo_confirmacao()  # Gera o código de 6 dígitos
        # print(request.form)
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #print(senha_cript)
        # Criar o usuario
        # adicionar na sessao
        # dar commit da sessao
        usuario = Usuario(username=form_criarconta.username.data, 
                          email=form_criarconta.email.data, 
                          senha=senha_cript, 
                          codigo_confirmacao=codigo_confirmacao)
        database.session.add(usuario)
        database.session.commit()
        enviar_email_confirmacao(usuario)  # Envia o e-mail de confirmação para o usuário
        flash('Um e-mail de confirmação foi enviado. Verifique sua caixa de entrada.', 'alert-success')  # Notifica o usuário
        # fazendo login do usuario
        # login_user(usuario)

        # Envia o e-mail de boas-vindas
        #enviar_email_bem_vindo(usuario)
        # exibir msg de conta criada com sucesso
        #flash(f'Conta Criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        # redirecionar para outra pagina
        # o return deve estar sempre atras do redirect(url_for('home'))
        return redirect(url_for("main.home"))

    # form_login=form_login, form_criarconta=form_criarconta está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


# pagina de sair
@auth_bp.route('/sair')
@login_required
def sair():
    # sair e redirecionar para a pagina home
    logout_user()
    flash('Logout feito com Sucesso', 'alert-success')
    return redirect(url_for('main.home'))


