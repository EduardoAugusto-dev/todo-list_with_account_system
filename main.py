from flask import Flask, render_template, Blueprint, redirect, url_for
from routes.todo import tasks
from routes.user import user
from models.database import db, User, Task
from flask_login import current_user, LoginManager, login_user, login_required
from datetime import date

app = Flask(__name__)
app.secret_key = 'GENERIC_KEY'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/')
@login_required
def home_page():
    tasks = Task.select().where(Task.user == current_user.id)
    print(f"Tasks: {tasks}")  
    return render_template('index.html', tasks=tasks)

def verificar_expiracao():
    tasks = Task.select()
    for task in tasks:
        task.update_status()

def blueprint_conf(app):
    app.register_blueprint(home)
    app.register_blueprint(user)
    app.register_blueprint(tasks)

blueprint_conf(app)

def db_config():
    db.connect()
    db.create_tables([User, Task], safe=True)

db_config()

@app.before_request
def before_request():
    if current_user.is_authenticated: 
        verificar_expiracao()

@app.route('/')
def homepage(): 
    return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(debug=True)
