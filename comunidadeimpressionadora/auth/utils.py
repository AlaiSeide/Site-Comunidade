
# Decorador para rotas que exigem que o usuário tenha o e-mail confirmado
def login_com_confirmacao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmado:  # Se o usuário não confirmou o e-mail
            flash('Por favor, confirme seu e-mail para acessar esta página.', 'alert-info')
            return redirect(url_for('unconfirmed'))  # Redireciona para a página de e-mail não confirmado
        return f(*args, **kwargs)
    return decorated_function
