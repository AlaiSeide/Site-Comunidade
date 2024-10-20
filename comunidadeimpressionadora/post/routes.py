from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required

from comunidadeimpressionadora.extensions import database
from comunidadeimpressionadora.post import post_bp
from comunidadeimpressionadora.forms import FormCriarPost
from comunidadeimpressionadora.model import Post


@post_bp.route('/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    formcriarpost = FormCriarPost()

    if formcriarpost.validate_on_submit():
        post = Post(titulo=formcriarpost.titulo.data, 
                    corpo=formcriarpost.corpo.data, 
                    autor=current_user
                )
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('main.home'))
    return render_template('posts/criarpost.html', formcriarpost=formcriarpost)


# O decorador @app.route é usado para associar uma URL a uma função específica.
# Neste caso, a URL é '/post/<post_id>'. '<post_id>' é uma variável na URL.
# Esta é a definição da função 'exibir_post'. Ela é chamada quando a URL acima é acessada.
# A função recebe um argumento, 'post_id', que é o valor da variável na URL.
@post_bp.route('/<post_id>', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('main.home'))
    else:
        formeditarpost = None

    # Aqui, estamos renderizando o template 'post.html' e passando o post e o formulário para o template.
    # Isso permitirá que você use os dados do post e do formulário no seu template.
    return render_template('posts/post.html', post=post, formeditarpost=formeditarpost)



# Esta linha define a rota para excluir um post. Ela aceita tanto métodos GET quanto POST.
@post_bp.route('/<int:post_id>/excluir', methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))

    # Se o usuário atual não for o autor do post, retornamos um erro 403 (Proibido).
    else:
        abort(403)

