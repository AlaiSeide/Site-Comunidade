from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from comunidadeimpressionadora.extensions import bcrypt, database

from comunidadeimpressionadora.auth import auth_bp
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, EsqueciSenhaForm, RedefinirSenhaForm
from comunidadeimpressionadora.model import Usuario

from comunidadeimpressionadora.mailer import enviar_email_de_confirmacao, gerar_codigo_confirmacao, validar_token_confirmacao_email, enviar_email_de_boas_vindas, enviar_email_confirmacao_de_redefinicao_de_senha

from comunidadeimpressionadora.password_reset import gerar_token, enviar_email, validar_token

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
        # Gera o código de 6 dígitos
        codigo_confirmacao = gerar_codigo_confirmacao() 
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

        # Envia o e-mail de confirmação para o usuário
        enviar_email_de_confirmacao(usuario)

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
    return render_template('auth/login.html', form_login=form_login, form_criarconta=form_criarconta)


# Rota para confirmar o e-mail usando o token e o código de confirmação
@auth_bp.route('/confirmar/<token>', methods=['GET', 'POST'])
def confirmar_email(token):
    form = ConfirmacaoEmailForm()  # Instancia o formulário de confirmação
    email = validar_token_confirmacao_email(token)  # Confirma o token e obtém o e-mail
    if not email:
        flash('O link de confirmação é inválido ou expirou.', 'alter-danger')  # Se o token for inválido ou expirado, mostra erro
        return redirect(url_for('auth.login'))  # Redireciona para o login

    usuario = Usuario.query.filter_by(email = email).first_or_404()  # Procura o usuário pelo e-mail no banco de dados
    if usuario.confirmado:  # Se o e-mail já foi confirmado, avisa o usuário
        flash('Conta já confirmada. Por favor, faça login.', 'alert-info')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():  # Se o formulário for enviado
        # Concatenar os valores dos campos do formulário para formar o código completo
        codigo_digitado = ''.join([
            form.code1.data,
            form.code2.data,
            form.code3.data,
            form.code4.data,
            form.code5.data,
            form.code6.data
        ])
        if codigo_digitado == usuario.codigo_confirmacao:  # Verifica se o código está correto
            usuario.confirmado = True  # Marca o usuário como confirmado
            usuario.data_confirmacao = datetime.now(timezone.utc)  # Salva a data de confirmação
            database.session.commit()  # Salva as mudanças no banco de dados
            enviar_email_de_boas_vindas(usuario)
            flash('Sua conta foi confirmada! Agora você pode fazer login.', 'alert-success')  # Mensagem de sucesso
            return redirect(url_for('auth.login'))  # Redireciona para a página de login
        else:
            flash('Código de confirmação inválido. Tente novamente.', 'alert-danger')  # Se o código estiver errado, mostra erro

    return render_template('auth/confirmar_codigo.html', form=form)  # Renderiza a página para inserir o código

# Rota para informar ao usuário que ele ainda não confirmou o e-mail
@auth_bp.route('/unconfirmed')
def unconfirmed():
    if current_user.is_authenticated and not current_user.confirmado:
        flash('Por favor, confirme seu e-mail.', 'alert-info')  # Avisa o usuário para confirmar o e-mail
    return render_template('auth/unconfirmed.html')  # Renderiza a página de confirmação pendente


@auth_bp.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if current_user.is_authenticated:
        return redirect(url_for('user.perfil'))
        
    form = EsqueciSenhaForm()  # Cria uma instância do formulário
    if form.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
        email = form.email.data  # Obtém o email do formulário
        # Procurar o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()  # Busca o usuário pelo email
        if usuario:
            # Gera um token para o usuário
            token = gerar_token(usuario)
            # Gera o link completo para redefinir a senha
            link = url_for('auth.redefinir_senha', token=token, _external=True)
            # Enviar o email
            enviar_email(
                email=usuario.email,
                assunto='Redefinição de Senha - Comunidade Impressionadora',
                template='email/email_redefinir_senha',
                usuario=usuario,
                link=link,
                ano_atual=datetime.now().year
            )
            flash('Um email foi enviado com instruções para redefinir sua senha.', 'alert-success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email não encontrado.', 'alert-danger')
            return redirect(url_for('auth.esqueci_senha'))
    return render_template('auth/esqueci_senha.html', form=form)


@auth_bp.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if current_user.is_authenticated:
        # Usuário já está logado, redirecionar para a página inicial ou perfil
        return redirect(url_for('main.home'))  # Substitua 'inicio' pela rota adequada
    """
    Rota para redefinir a senha usando o token recebido.
    """
    # Valida o token
    token_obj = validar_token(token)
    if not token_obj:
            # Se o token for inválido ou expirou, exibe uma mensagem de erro
            flash('O link é inválido ou expirou.', 'alert-danger')
            return redirect(url_for('auth.esqueci_senha'))
    
    # Busca o usuário associado ao token pelo id desse usuario
    usuario = Usuario.query.get(token_obj.usuario_id)

    if not usuario:
        # Se o usuário não for encontrado, exibe uma mensagem de erro
        flash('Usuário não encontrado.', 'alert-danger')
        return redirect(url_for('auth.esqueci_senha'))
    
    form = RedefinirSenhaForm()  # Cria uma instância do formulário de redefinição de senha

    if form.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
        if bcrypt.check_password_hash(usuario.senha, form.senha.data):  # Comparação com o usuário buscado pelo token
            flash('A nova senha não pode ser igual à antiga.', 'alert-danger')
        else:
            nova_senha = form.senha.data  # Obtém a nova senha do formulário
            
            # Atualiza a senha do usuário utilizando Flask-Bcrypt
            usuario.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
            
            # Marca o token como usado para evitar reuso
            token_obj.usado = True
            
            # Salva as alterações no banco de dados
            database.session.commit()
            
            # Envia o e-mail de confirmação de redefinição de senha
            enviar_email_confirmacao_de_redefinicao_de_senha(usuario)

            # Exibe uma mensagem de sucesso
            flash('Sua senha foi redefinida com sucesso!', 'alert-success')
            return redirect(url_for('main.home'))
    
    # Renderiza o formulário de redefinir_senha.html
    return render_template('auth/redefinir_senha.html', form=form)


# pagina de sair
@auth_bp.route('/sair')
@login_required
def sair():
    # sair e redirecionar para a pagina home
    logout_user()
    flash('Logout feito com Sucesso', 'alert-success')
    return redirect(url_for('main.home'))


