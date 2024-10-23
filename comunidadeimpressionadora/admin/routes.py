from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from comunidadeimpressionadora.extensions import bcrypt, database
from comunidadeimpressionadora.admin import admin_bp
from comunidadeimpressionadora.forms import FormLogin
from comunidadeimpressionadora.model import Usuario

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Lógica de login aqui
    pass

@admin_bp.route('/logout')
def logout():
    # Lógica de logout aqui
    pass

@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Lógica de registro de usuário aqui
    pass
