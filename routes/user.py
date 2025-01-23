from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from models.database import User, db
from peewee import IntegrityError
from models.database import User
from models.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/register', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'status': 'error', 'message': "Please fill in all fields!"})


        if User.select().where(User.email == email).exists():
            return jsonify({'status': 'error', 'message': "This email is already registered."})

        username = email.split('@')[0] 

        hashed_password = generate_password_hash(password)
        try:
            with db.atomic():
                User.create(email=email, password=hashed_password, username=username)
                return redirect(url_for('user.login'))

        except IntegrityError as e:
            return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"})

    return render_template('register.html')


# Rota para login
@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Todos os campos são obrigatórios!", "error")
            return render_template('login.html')

        user = User.get_or_none(User.email == email)
        if not user or not check_password_hash(user.password, password):
            flash("Email ou senha inválidos!", "error")
            return render_template('login.html')

        login_user(user)  
        return redirect(url_for('home.home_page'))

    return render_template('login.html')


@user.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user_id',None)
    return redirect(url_for('user.login'))

    return render_template('index.html')

