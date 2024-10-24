from flask import Flask
from comunidadeimpressionadora.config import Config
from comunidadeimpressionadora.extensions import database, bcrypt, login_manager, mail, csrf, migrate, limiter
from comunidadeimpressionadora.forms import LogoutForm  # Certifique-se de que o caminho está correto
import os
from dotenv import load_dotenv
import ssl
import certifi
# Carregar o .env
load_dotenv()

# Inicializando o Flask diretamente
app = Flask(__name__)
# Configurações do reCAPTCHA e do Flask, pegando do .env
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')


# ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Carregar as configurações da aplicação
app.config.from_object(Config)

# Inicializar as extensões
csrf.init_app(app)
database.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
migrate.init_app(app, database)
# Define um processador de contexto global para injetar o formulário de logout em todos os templates.
# Isso permite que o formulário de logout, incluindo o token CSRF, esteja disponível automaticamente
# em todas as páginas da aplicação, sem a necessidade de passá-lo manualmente em cada rota.
# O formulário é usado principalmente na barra de navegação para que o usuário possa realizar logout de forma segura.
# Define um processador de contexto global
@app.context_processor
def inject_logout_form():
    form_logout = LogoutForm()
    return dict(form_logout=form_logout)

# Registrando os blueprints
from comunidadeimpressionadora.main import main_bp
from comunidadeimpressionadora.auth import auth_bp
from comunidadeimpressionadora.user import user_bp
from comunidadeimpressionadora.post import post_bp
from comunidadeimpressionadora.admin import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(admin_bp, url_prefix='/admin')



# Aplicar o limiter ao app
limiter.init_app(app)