from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from models.database import User, db
from peewee import IntegrityError
from models.database import User
from models.database import db

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/register', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'status': 'error', 'message': "Please fill in all fields!"})

        if User.select().where(User.email == email).exists():
            return jsonify({'status': 'error', 'message': "This email already exists, try something different."})

        try:
            with db.atomic():
                db_user = User.create(email=email, password=password, username = username)
            return jsonify({
                'status': 'success',
                'message': "User created succesfully!",
                'user_id': db_user.id
                })

        except IntegrityError as e:
            return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"})

    return render_template('register.html')


@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'status': 'error', 'message': "All fields are required!"})

        user = User.get_or_none(User.email == email, User.password == password)
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home.home_page'))

        else:
            return jsonify({'status': 'error', 'message': "Invalid credentials!"})

    return render_template('login.html')
