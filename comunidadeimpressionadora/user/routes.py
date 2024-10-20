from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user

from comunidadeimpressionadora.extensions import database, bcrypt
from comunidadeimpressionadora.user import user_bp
from comunidadeimpressionadora.forms import FormEdiarPerfil, AlterarSenhaForm, ConfirmarExclusaoContaForm
from comunidadeimpressionadora.model import Usuario
from comunidadeimpressionadora.mailer import enviar_email_alteracao_senha, enviar_email_exclusao_conta
from .utils import salvar_imagem, atualizar_cursos

@user_bp.route('/perfil')
@login_required
def perfil():
    foto_perfil = f'/static/fotos_perfil/{current_user.foto_perfil}'
    # foto_perfil = url_for(f'static', filename='fotos_perfil/{current_user.foto_perfil}')
    return render_template('user/perfil.html', foto_perfil=foto_perfil)


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
        return redirect(url_for('user.perfil'))
    
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
    return render_template('user/editarperfil.html', foto_perfil=foto_perfil, formeditarperfil=formeditarperfil)


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
        return redirect(url_for('user.perfil'))
    return render_template('auth/alterar_senha.html', form=form)


@user_bp.route('/confirmar_exclusao', methods=['GET', 'POST'])
@login_required
def confirmar_exclusao():
    form = ConfirmarExclusaoContaForm()
    if form.validate_on_submit():
        # Verificar se a senha está correta
        if not bcrypt.check_password_hash(current_user.senha, form.senha.data):
            flash('Senha incorreta. Tente novamente.', 'alert-danger')
            return redirect(url_for('user.confirmar_exclusao'))
        
        # Verificar se o checkbox foi marcado
        if not form.confirmacao.data:
            flash('Você deve marcar a caixa de confirmação para excluir sua conta.', 'alert-danger')
            return redirect(url_for('user.confirmar_exclusao'))
        
        # Excluir a conta
        usuario = current_user
        enviar_email_exclusao_conta(usuario)
        database.session.delete(usuario)
        database.session.commit()
        
        # Fazer logout
        logout_user()
        
        flash('Sua conta foi excluída com sucesso.', 'alert-success')
        return redirect(url_for('main.home'))

    return render_template('user/confirmar_exclusao.html', form=form)