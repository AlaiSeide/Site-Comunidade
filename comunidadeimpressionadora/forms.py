# Arquivo de formularios
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from comunidadeimpressionadora.models import Usuario
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
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')



class FormEdiarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
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
