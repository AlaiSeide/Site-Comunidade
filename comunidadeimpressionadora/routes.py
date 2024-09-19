from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt, mail
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEdiarPerfil, ContatoForm, FormCriarPost, DeleteAccountForm
from comunidadeimpressionadora.models import Usuario, Contato, Post, TokenRedefinicao
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from datetime import datetime
import uuid
from datetime import datetime, timedelta, timezone

# pagina principal
@app.route("/")
def home():
    # ordenar os post do recentes para mais antigos order_by(Post.id.desc())
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


# pagina de contato
@app.route("/contato", methods=['GET', 'POST'])
def contato():
        contatoform = ContatoForm()
        if contatoform.validate_on_submit():
            contato = Contato(nome=contatoform.nome.data, email=contatoform.email.data, mensagem=contatoform.mensagem.data)

            database.session.add(contato)
            database.session.commit()
            print(request.form)
            print(request.method)
            print(request.full_path)
            print(request.args)
            flash('Sua mensagem foi enviada com sucesso!', 'alert-success')
        elif request.method == 'GET' and current_user.is_authenticated:
           contatoform.nome.data = current_user.username
           contatoform.email.data = current_user.email

        # Configuração do email
        # meu_email = "alaiseide2006@gmail.com"  # Substitua pelo seu email
        # minha_senha = "Flashrevers20102010.."  # Substitua pela sua senha

        # # Criar a mensagem
        # msg = MIMEMultipart()
        # msg['From'] = meu_email
        # msg['To'] = meu_email  # Você pode substituir por qualquer outro email
        # msg['Subject'] = "Nova mensagem de contato"
        # corpo_email = f"Nome: {contatoform.nome.data}\nEmail: {contatoform.email.data}\nMensagem:\n{contatoform.mensagem.data}"
        # msg.attach(MIMEText(corpo_email, 'plain'))

        # # Enviar o email
        # server = smtplib.SMTP('smtp.gmail.com', 587)  # Use o servidor SMTP do seu provedor de email
        # server.starttls()
        # server.login(meu_email, minha_senha)
        # text = msg.as_string()
        # server.sendmail(meu_email, meu_email, text)
        # server.quit()
        # Aqui você pode adicionar o código para lidar com os dados do formulário de contato
        # Por exemplo, você pode enviar um e-mail com a mensagem ou armazená-la em um banco de dados

        return render_template('contato.html', contatoform=contatoform)

# pagina de usuarios
@app.route("/usuarios")
@login_required
def usuarios():
    # meus_usuarios=lista_usuarios está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html

    # pegando todos os usuarios do meu banco de dados 
    lista_usuarios = Usuario.query.all()
    ## print(lista_usuarios)
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

            
        """
        request.form é um dicionário que contém todos os campos do formulário. A chave é o nome do campo e o valor é o valor do campo. Então, 'botao_submit_criarconta' in request.form verifica se a chave 'botao_submit_criarconta' está presente no dicionário request.form, o que significaria que o botão de submit do formulário de criação de conta foi pressionado."""
   
    # Verifica se o usuario criou conta com sucesso
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # print(request.form)
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #print(senha_cript)
        # Criar o usuario
        # adicionar na sessao
        # dar commit da sessao
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        # fazendo login do usuario
        login_user(usuario)
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
    delete_account_form = DeleteAccountForm()
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil, delete_account_form=delete_account_form)

# pagina de criar post
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    formcriarpost = FormCriarPost()

    if formcriarpost.validate_on_submit():
        post = Post(titulo=formcriarpost.titulo.data, corpo=formcriarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', formcriarpost=formcriarpost)


# uma funcao que vai fazer todas as validacoes da imagem e salvar-la
def salvar_imagem(imagem):
    # adicionar um codigo aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    # separar o nome do arquivo com a extensao
    nome, extensao = os.path.splitext(imagem.filename)
    # juntar nome, codigo e a extensao
    nome_arquivo = nome + codigo + extensao
    # salvar a imagem na pasta fotos_perfil
    #  o app.root_path seria o caminho do novo app que é comunidadeimpressionadora
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    # 200x200 px
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuario para o novo nome
    return nome_arquivo

# uma funcao para atualizar os cursos 
def atualizar_cursos(formulario):
    lista_cursos = []
    # percorrer todos os campos de cursos do formulario
    for campo in formulario:
        # verifica se o campo do formulario comeca com curso_
        if 'curso_' in campo.name:
            # verificar se o campo for marcado
            if campo.data:
                # adicionar o texto do campo.label  (Excel Impressionador) na lista de cursos
                lista_cursos.append(campo.label.text)
    # Então, se lista_cursos fosse ['Curso1', 'Curso2', 'Curso3'], a linha de código retornaria a string 'Curso1;Curso2;Curso3'. Espero que isso esclareça! Se você tiver mais perguntas, fique à vontade para
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    delete_account_form = DeleteAccountForm()
    # uma instancia da minha classe FormEdiarPerfil
    formeditarperfil = FormEdiarPerfil()
    # validar o meu formulario
    if formeditarperfil.validate_on_submit():
        # mudar o email e o username do usuario
        current_user.email = formeditarperfil.email.data
        current_user.username = formeditarperfil.username.data
        # verificar se eu tenho que mudar a foto de perfil
        if formeditarperfil.foto_perfil.data:
            # adicionar um codigo aleatorio no nome da imagem
            # reduzir o tamanho da imagem
            # salvar a imagem na pasta fotos_perfil
            # mudar o campo foto_perfil do usuario para o novo nome da imagem
            nome_imagem = salvar_imagem(formeditarperfil.foto_perfil.data)
            #print(formeditarperfil.foto_perfil.data)
            # mudar a foto do perfil
            current_user.foto_perfil = nome_imagem
        # Atualizar os cursos do usuarios
        current_user.cursos = atualizar_cursos(formeditarperfil)

        database.session.commit()
        flash(f'Perfil Atualizado com Sucesso', 'alert-success')
        # redirecionar para a pagina do perfil dele
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
    return render_template('editarperfil.html', foto_perfil=foto_perfil, formeditarperfil=formeditarperfil, delete_account_form=delete_account_form)




# O decorador @app.route é usado para associar uma URL a uma função específica.
# Neste caso, a URL é '/post/<post_id>'. '<post_id>' é uma variável na URL.
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
# Esta é a definição da função 'exibir_post'. Ela é chamada quando a URL acima é acessada.
# A função recebe um argumento, 'post_id', que é o valor da variável na URL.
def exibir_post(post_id):

    # Aqui, 'Post.query.get(post_id)' está fazendo uma consulta ao banco de dados para obter o post com o id especificado.
    # 'Post' é presumivelmente uma classe que representa uma postagem no seu banco de dados.
    # 'query' é um objeto que permite fazer consultas ao banco de dados.
    # 'get(post_id)' está buscando o post com o id especificado.
    post = Post.query.get(post_id)

    # Aqui, estamos verificando se o usuário atual é o autor do post.
    # Se for, criamos um novo formulário de edição de post.
    # Se não for, definimos 'form' como None. Isso pode ser útil para controlar o que é exibido para o usuário na página.
    if current_user == post.autor:

        formeditarpost = FormCriarPost()
        if request.method == 'GET':
            # preencher os campos de titulo e corpo  automaticamente
            formeditarpost.titulo.data = post.titulo
            formeditarpost.corpo.data = post.corpo

        elif formeditarpost.validate_on_submit():
            # formeditarpost.titulo.data é o formulario que o cara preencheu
            post.titulo = formeditarpost.titulo.data
            post.corpo = formeditarpost.corpo.data
            # posso dar so database.session.commit() porque ele ja existe no meu banco de dados
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        formeditarpost = None

    # Aqui, estamos renderizando o template 'post.html' e passando o post e o formulário para o template.
    # Isso permitirá que você use os dados do post e do formulário no seu template.
    return render_template('post.html', post=post, formeditarpost=formeditarpost)


# Esta linha define a rota para excluir um post. Ela aceita tanto métodos GET quanto POST.
@app.route('/post/<int:post_id>/excluir', methods=['GET', 'POST'])
# O decorador @login_required garante que o usuário deve estar logado para acessar esta rota.
@login_required
# Esta é a função que será chamada quando a rota acima for acessada.
def excluir_post(post_id):


    # Aqui, estamos buscando o post com o id especificado do banco de dados.
    post = Post.query.get(post_id)

    # Verificamos se o usuário atual é o autor do post.
    if current_user == post.autor:

        # Se for, excluímos o post do banco de dados e confirmamos a transação.
        database.session.delete(post)
        database.session.commit()

        # Exibimos uma mensagem para o usuário informando que o post foi excluído com sucesso.
        flash('Post Excluido com Sucesso', 'alert-danger')

        # Redirecionamos o usuário para a página inicial.
        return redirect(url_for('home'))

    # Se o usuário atual não for o autor do post, retornamos um erro 403 (Proibido).
    else:
        abort(403)


@app.route('/configuracoes')
def configuracoes():
    return render_template('configuracoes.html')

@app.route('/set_language/<language>')
def set_language(language):
    response = redirect(url_for('home'))  # Redireciona para a página inicial depois de mudar o idioma
    response.set_cookie('lang', language)  # Define um cookie com o idioma escolhido
    return response




# unção para gerar o token
# Vamos criar uma função que cria uma chave especial para o usuário:
# def gerar_token(usuario):
#     s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     return s.dumps({'usuario_id': usuario.id})

def gerar_token(usuario):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token_str = s.dumps({'usuario_id': usuario.id})
    token = TokenRedefinicao(
        token=token_str,
        usuario_id=usuario.id,
        data_expiracao=datetime.now(timezone.utc) + timedelta(hours=1)  # expira em 1 hora
    )
    database.session.add(token)
    database.session.commit()
    return token_str

def validar_token(token_str):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        dados = s.loads(token_str, max_age=3600)
        token = TokenRedefinicao.query.filter_by(token=token_str).first()
        if token and not token.usado and token.data_expiracao >= datetime.now(timezone.utc):
            return token
        else:
            return None
    except:
        return None


# def enviar_email(email, token):
#     link = url_for('redefinir_senha', token=token, _external=True)
#     # Aqui você configuraria seu serviço de email para enviar o link
#     # Por simplicidade, vamos só imprimir o link
#     print(f'Clique no link para redefinir sua senha: {link}')

def enviar_email(email, assunto, template, **kwargs):
    msg = Message(assunto, sender='noreply@comunidadeimpressionadora.com', recipients=[email])
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


##############
# Usuário diz que esqueceu a senha.
# Nós enviamos um link especial para o email dele.
# Ele clica no link e escolhe uma nova senha.
# Atualizamos a senha na nossa caixinha.

# Página para o usuário dizer que esqueceu a senha

# @app.route('/esqueci_senha', methods=['GET', 'POST'])
# def esqueci_senha():
#     if current_user.is_authenticated:
#         # Usuário já está logado, redirecionar para a página inicial ou perfil
#         return redirect(url_for('perfil'))  # Substitua 'inicio' pela rota adequada

#     if request.method == 'POST':
#         email = request.form['email']
#         # Aqui vamos procurar o usuário pelo email
#         usuario = Usuario.query.filter_by(email=email).first()
#         # se existir usuario
#         if usuario:
#             # Criar um token (chave especial)
#             token = gerar_token(usuario)
#             # Enviar o email com o link mágico
#             enviar_email(usuario.email, token)
#             flash('Um email foi enviado com instruções para redefinir sua senha.', 'alert-success')
#         else:
#             flash('Email não encontrado.', 'alert-info')
#         return redirect(url_for('login'))
#     return render_template('esqueci_senha.html')

@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))
    if request.method == 'POST':
        email = request.form['email']
        # Procurar o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            # Criar um token
            token = gerar_token(usuario)
            # Gerar o link de redefinição de senha
            link = url_for('redefinir_senha', token=token, _external=True)
            # Enviar o email
            enviar_email(
                email=usuario.email,
                assunto='Redefinição de Senha - Comunidade Impressionadora',
                template='email_redefinir_senha',
                usuario=usuario,
                link=link,
                ano_atual=datetime.now().year
            )
            flash('Um email foi enviado com instruções para redefinir sua senha.', 'alert-success')
            return redirect(url_for('login'))
        else:
            flash('Email não encontrado.', 'alert-danger')
            return redirect(url_for('esqueci_senha'))
    return render_template('esqueci_senha.html')


def gerar_hash(senha):
    return bcrypt.generate_password_hash(senha)

@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if current_user.is_authenticated:
        # Usuário já está logado, redirecionar para a página inicial ou perfil
        return redirect(url_for('home'))  # Substitua 'inicio' pela rota adequada

    dados = validar_token(token)
    if not dados:
        flash('O link para redefinir a senha é inválido ou expirou.', 'alert-danger')
        return redirect(url_for('esqueci_senha'))

    usuario = Usuario.query.get(dados['usuario_id'])

    if request.method == 'POST':
        nova_senha = request.form['senha']
        usuario.senha = gerar_hash(nova_senha)  # Função para criptografar a senha
        database.session.commit()
        flash('Sua senha foi atualizada!', 'alert-success')
        return redirect(url_for('login'))
    
    # Marcar o token como usado
    token.usado = True
    database.session.commit()

    return render_template('redefinir_senha.html')


@app.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    if request.method == 'POST':
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']

        # Verificar se a senha atual está correta
        if bcrypt.check_password_hash(current_user.senha, senha_atual):
            # Verificar se a nova senha é diferente da atual
            if not bcrypt.check_password_hash(current_user.senha, nova_senha):
                # Aqui você pode adicionar verificações adicionais para a força da senha
                current_user.senha = gerar_hash(nova_senha)
                database.session.commit()
                flash('Sua senha foi atualizada com sucesso!', 'alert-success')
                return redirect(url_for('perfil'))
            else:
                flash('A nova senha não pode ser igual à senha atual.', 'alert-info')
        else:
            flash('Senha atual incorreta.', 'alert-danger')
    return render_template('alterar_senha.html')


# @app.route('/excluir_conta', methods=['GET', 'POST'])
# @login_required
# def excluir_conta():
#     form = DeleteAccountForm()
#     if form.validate_on_submit():
#         user = Usuario.query.get(current_user.id)
#         database.session.delete(user)
#         database.session.commit()
#         logout_user()
#         flash('Sua conta e todo o seu conteúdo foram excluídos.', 'alert-success')
#         return redirect(url_for('home'))
#     return render_template('excluir_conta.html', form=form)

@app.route('/excluir_conta',  methods=['GET', 'POST'])
@login_required
def excluir_conta():
    delete_account_form = DeleteAccountForm()
    if delete_account_form.validate_on_submit():
        user = Usuario.query.get(current_user.id)
        print(user)
        database.session.delete(user)
        database.session.commit()
        logout_user()
        flash('Sua conta e todo o seu conteúdo foram excluídos.', 'alert-success')
        return redirect(url_for('home'))
    else:
        flash('Requisição inválida.', 'alert-danger')
        return redirect(url_for('perfil'))