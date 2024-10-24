
# Decorador para rotas que exigem que o usuário tenha o e-mail confirmado
def login_com_confirmacao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmado:  # Se o usuário não confirmou o e-mail
            flash('Por favor, confirme seu e-mail para acessar esta página.', 'alert-info')
            return redirect(url_for('unconfirmed'))  # Redireciona para a página de e-mail não confirmado
        return f(*args, **kwargs)
    return decorated_function


from datetime import datetime  # Para obter a data e hora atual
from flask import flash, redirect, url_for  # Para mensagens flash e redirecionamento
from datetime import timedelta  # Para definir o intervalo de tempo entre reenvios

# Definindo o intervalo de reenvio (por exemplo, 10 minutos)
INTERVALO_REENVIO = timedelta(minutes=10)

def verificar_intervalo_reenvio(usuario):
    """
    Verifica se o usuário solicitou o reenvio do e-mail de confirmação recentemente.

    Se o usuário já tiver solicitado o reenvio do e-mail de confirmação dentro de um intervalo
    de tempo definido (por exemplo, 10 minutos), calcula o tempo restante até que ele possa
    solicitar novamente e retorna um redirecionamento com uma mensagem informando o usuário.

    Parâmetros:
        usuario (Usuario): O objeto do usuário que está solicitando o reenvio.

    Retorna:
        redirect: Redireciona para a rota de reenvio de confirmação com uma mensagem flash
                  se o intervalo mínimo não tiver sido atingido.
        None: Se o usuário puder solicitar o reenvio, a função retorna None.
    """
    # Verifica se o usuário já solicitou o reenvio recentemente
    if usuario.ultimo_envio_confirmacao and datetime.utcnow() < usuario.ultimo_envio_confirmacao + INTERVALO_REENVIO:
        # Calcula o tempo restante até que o usuário possa solicitar novamente
        tempo_restante = (usuario.ultimo_envio_confirmacao + INTERVALO_REENVIO) - datetime.utcnow()
        minutos_restantes = int(tempo_restante.total_seconds() // 60) + 1  # Arredonda para cima
        # Informa o usuário sobre o tempo restante
        flash(f'Você já solicitou um reenvio recentemente. Tente novamente em {minutos_restantes} minutos.', 'alert-warning')
        # Redireciona o usuário para a rota de reenvio de confirmação
        return redirect(url_for('auth.reenviar_confirmacao'))
    # Se o usuário puder solicitar o reenvio, a função não retorna nada
    return None