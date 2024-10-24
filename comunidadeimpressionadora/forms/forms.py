# Arquivo de formularios
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from comunidadeimpressionadora.model import Usuario, Contato
from flask_login import current_user
from comunidadeimpressionadora.extensions import bcrypt
from .validators import validar_senha, validar_email_temporario, validar_email_dns #, validar_email_unico

# Formularios de criar conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    recaptcha = RecaptchaField()  # Adiciona o campo de reCAPTCHA
    botao_submit_criarconta = SubmitField('Criar Conta')


    def validate_senha(self, senha):
        validar_senha(senha.data, username=self.username.data, email=self.email.data)

    # funcao de validacao para um email unico no banco de dados
    def validate_email(self, email):
        # Validação de e-mail único
        # validar_email_unico(email)
        
        # Validação para impedir domínios temporários
        validar_email_temporario(email)
        
        # Validação DNS para garantir que o domínio tem registros MX
        validar_email_dns(email)

# formularios de fazer login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    mostrar_senha = BooleanField('Mostrar Senha')
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    recaptcha = RecaptchaField()  # Adiciona o campo de reCAPTCHA
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

class ConfirmarExclusaoContaForm(FlaskForm):
    senha = PasswordField('Senha', validators=[DataRequired()])  # Campo para a senha
    confirmacao = BooleanField('Eu confirmo que quero excluir a conta.', validators=[DataRequired()])  # Checkbox de confirmação
    submit = SubmitField('Excluir Conta')


# Definição dos formulários

class EsqueciSenhaForm(FlaskForm):
    """
    Formulário para solicitar a redefinição de senha.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo para digitar o email
    submit = SubmitField('Enviar')  # Botão para enviar o formulário

class RedefinirSenhaForm(FlaskForm):
    """
    Formulário para redefinir a senha.
    """
    senha = PasswordField('Nova Senha', validators=[DataRequired()])  # Campo para a nova senha
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('senha')])  # Campo para confirmar a senha
    submit = SubmitField('Redefinir Senha')  # Botão para enviar a nova senha

    # nao funciona porque o usuario nao esta logado, e o current_user so sabe a senha do usuario se ele estiver logado.
    # def validate_senha(self, senha):
    #     # Aqui você busca o usuário atual no banco e verifica se a nova senha é igual à antiga
    #     if bcrypt.check_password_hash(current_user.senha, senha):
    #         raise ValidationError('A nova senha não pode ser igual à antiga.')


class AlterarSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=8, message='A senha deve ter pelo menos 8 caracteres.')])
    confirmar_nova_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('nova_senha', message='As senhas devem corresponder.')])
    submit = SubmitField('Alterar Senha')

    def validate_nova_senha(self, nova_senha):
        # se a senha atual é igual a nova senha que o usuario digitou no formulario
        if bcrypt.check_password_hash(current_user.senha, nova_senha.data):
            raise ValidationError('A nova senha não pode ser igual à senha atual.')

    def validate_senha_atual(self, senha_atual):
        # se a senha atual é diferente da senha s´do usuario que está armazenado no banco de dados.
        if not bcrypt.check_password_hash(current_user.senha, senha_atual.data):
            raise ValidationError('Senha atual incorreta.')
        
# Formulário para o usuário inserir o código de confirmação
class ConfirmacaoEmailForm(FlaskForm):
   # Criamos 6 campos de um dígito para o código de confirmação
    code1 = StringField('Código 1', validators=[DataRequired(), Length(min=1, max=1)])
    code2 = StringField('Código 2', validators=[DataRequired(), Length(min=1, max=1)])
    code3 = StringField('Código 3', validators=[DataRequired(), Length(min=1, max=1)])
    code4 = StringField('Código 4', validators=[DataRequired(), Length(min=1, max=1)])
    code5 = StringField('Código 5', validators=[DataRequired(), Length(min=1, max=1)])
    code6 = StringField('Código 6', validators=[DataRequired(), Length(min=1, max=1)])
    
    submit = SubmitField('Confirmar')

# class ConfirmarExclusaoContaForm(FlaskForm):


class ReenviarConfirmacaoForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Reenviar Confirmação')

class LogoutForm(FlaskForm):
    submit = SubmitField('Sair')

class FormVerificacao2FA(FlaskForm):
    codigo = StringField('Código de Verificação', validators=[DataRequired(), Length(6, 6)])  # O código é sempre de 6 dígitos
    botao_submit_verificacao = SubmitField('Verificar')