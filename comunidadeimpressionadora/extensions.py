from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Inicializar as extensões
database = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
migrate = Migrate()

# Configurações do login_manager
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página, por favor.'
login_manager.login_message_category = 'alert-info'
