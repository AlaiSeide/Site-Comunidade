# Arquivo de formularios
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from comunidadeimpressionadora.models import Usuario, Contato
from flask_login import current_user

# Formularios de criar conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # funcao de validacao para um email unico no banco de dados
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


# formularios de fazer login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    mostrar_senha = BooleanField('Mostrar Senha')
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')



class FormEdiarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos .jpg e .png são permitidos.')])

    curso_excel = BooleanField('Excel Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_java = BooleanField('Java Impressionador')
    curso_javascript = BooleanField('JavaScript Impressionador')
    curso_csharp = BooleanField('C# Impressionador')
    curso_ruby = BooleanField('Ruby Impressionador')

    botao_submit_editarperfil = SubmitField('Corfirmar Edicao')

    # funcao de validacao antes de mudar o email do usuario
    def validate_email(self, email):
        """Essa função é usada para validar se um novo e-mail fornecido em um formulário de registro já está sendo usado por outro usuário. Se um usuário diferente já estiver registrado com o e-mail fornecido, uma mensagem de erro é gerada para informar ao usuário que ele deve fornecer um e-mail único.
        """
        # verificar se o cara mudou o email
        # se o email do usuario atual é diferente do email que ele preencheu
        # Verifica se o e-mail fornecido no formulário de registro é diferente do e-mail atual do usuário logado.
        if current_user.email != email.data:
            # Se o e-mail fornecido é diferente, busca no banco de dados se já existe um usuário com o mesmo e-mail.
            usuario = Usuario.query.filter_by(email=email.data).first()
            # Se um usuário com o mesmo e-mail é encontrado, lança uma exceção de validação com uma mensagem de erro.
            if usuario:
                raise ValidationError('Já existe um usuário com esse E-mail. Por favor, cadastre outro E-mail.')
            



class ContatoForm(FlaskForm):

    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

            
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    submit = SubmitField('Enviar')

    def validate_email(self, email):
        usuario = Contato.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Voce ja tinha enviado uma Mensagem espera até ser respondida...')

    # def validate_email(self, email):
    #     if current_user.is_authenticated:
    #         usuario = Contato.query.filter_by(email=email.data).first()
            
    #         if usuario:
    #             raise ValidationError('Voce ja tinha enviado uma Mensagem espera até ser respondida...')
    #     else:
    #         usuario = Contato.query.filter_by(email=email.data).first()
    #         if usuario:
    #             raise ValidationError('Voce ja tinha enviado uma Mensagem espera até ser respondida...')


class FormCriarPost(FlaskForm):

    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')

class DeleteAccountForm(FlaskForm):
   pass  # Não precisa adicionar campos, mas mantém o CSRF ativo