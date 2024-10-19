from flask import render_template
from comunidadeimpressionadora.main import main_bp
from comunidadeimpressionadora.models import Post

@main_bp.route('/')
def home():
    # Busca todos os posts e ordena-os do mais recente para o mais antigo
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)
