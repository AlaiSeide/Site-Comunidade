from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from comunidadeimpressionadora import database, bcrypt
from comunidadeimpressionadora.user import user_bp
from comunidadeimpressionadora.forms import FormEdiarPerfil, AlterarSenhaForm
from comunidadeimpressionadora.models import Usuario


@user_bp.route('/perfil')
@login_required
def perfil():
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@user_bp.route('/perfil/editar', methods=['GET', 'POST'])
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

# pagina de usuarios
@user_bp.route("/usuarios")
@login_required
def usuarios():
    # meus_usuarios=lista_usuarios está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html

    # pegando todos os usuarios do meu banco de dados 
    lista_usuarios = Usuario.query.all()
    ## print(lista_usuarios)
    return render_template('usuarios.html', meus_usuarios=lista_usuarios)



# pagina de contato
@app.route("/contato", methods=['GET', 'POST'])
def contato():
        contatoform = ContatoForm()
        if contatoform.validate_on_submit():
            contato = Contato(
                            nome=contatoform.nome.data,
                            email=contatoform.email.data,
                            mensagem=contatoform.mensagem.data
                        )

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



@user_bp.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        # As validações já são tratadas no formulário
        # Atualiza a senha do usuário
        # codifica a senha que o usuario digitou no formulario
        nova_senha_hash = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')
        # muda a senha o usuario
        current_user.senha_hash = nova_senha_hash
        database.session.commit()
        # Envia o e-mail de notificação de alteração de senha
        enviar_email_alteracao_senha(current_user)
        flash('Sua senha foi atualizada com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    return render_template('alterar_senha.html', form=form)


@user_bp.route('/confirmar_exclusao', methods=['GET', 'POST'])
@login_required
def confirmar_exclusao():
    form = ConfirmarExclusaoContaForm()
    if form.validate_on_submit():
        # Verificar se a senha está correta
        if not bcrypt.check_password_hash(current_user.senha, form.senha.data):
            flash('Senha incorreta. Tente novamente.', 'alert-danger')
            return redirect(url_for('confirmar_exclusao'))
        
        # Verificar se o checkbox foi marcado
        if not form.confirmacao.data:
            flash('Você deve marcar a caixa de confirmação para excluir sua conta.', 'alert-danger')
            return redirect(url_for('confirmar_exclusao'))
        
        # Excluir a conta
        usuario = current_user
        enviar_email_exclusao_conta(usuario)
        database.session.delete(usuario)
        database.session.commit()
        
        # Fazer logout
        logout_user()
        
        flash('Sua conta foi excluída com sucesso.', 'alert-success')
        return redirect(url_for('home'))

    return render_template('confirmar_exclusao.html', form=form)