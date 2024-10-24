from flask import render_template, flash, request
from flask_login import login_required, current_user

from comunidadeimpressionadora.extensions import database
from comunidadeimpressionadora.main import main_bp
from comunidadeimpressionadora.model import Post, Usuario
from comunidadeimpressionadora.forms import ContatoForm, LogoutForm

@main_bp.route('/')
def home():
    # Busca todos os posts e ordena-os do mais recente para o mais antigo
    posts = Post.query.order_by(Post.id.desc()).all()
    form = LogoutForm()  # Instancia o formulário
    return render_template('home.html', posts=posts, form=form)


# pagina de usuarios
@main_bp.route("/usuarios")
@login_required
def usuarios():
    # meus_usuarios=lista_usuarios está dentro da minha funcao render_template() para poderem ser mostrados dentro da minha pagina html

    # pegando todos os usuarios do meu banco de dados 
    lista_usuarios = Usuario.query.all()
    ## print(lista_usuarios)
    return render_template('user/usuarios.html', meus_usuarios=lista_usuarios)


# pagina de contato
@main_bp.route("/contato", methods=['GET', 'POST'])
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

        return render_template('user/contato.html', contatoform=contatoform)



@main_bp.route('/politica_privacidade')
@login_required
def politica_privacidade():
    return render_template('pages/politica_privacidade.html')


@main_bp.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('pages/configuracoes.html')