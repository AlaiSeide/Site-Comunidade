from flask import Flask
from comunidadeimpressionadora.config import Config
from comunidadeimpressionadora.extensions import database, bcrypt, login_manager, mail, csrf, migrate, limiter



# Inicializando o Flask diretamente
app = Flask(__name__)


# Carregar as configurações da aplicação
app.config.from_object(Config)

# Inicializar as extensões
csrf.init_app(app)
database.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
migrate.init_app(app, database)

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