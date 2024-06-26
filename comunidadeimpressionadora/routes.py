from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEdiarPerfil, ContatoForm, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Contato, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

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
    return render_template('editarperfil.html', foto_perfil=foto_perfil, formeditarperfil=formeditarperfil)




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