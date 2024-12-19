from flask import Flask, render_template, Blueprint, redirect, url_for
from routes.todo import tasks
from routes.user import user
from models.database import db, User, Task
from flask_login import current_user, LoginManager, login_user

app = Flask(__name__)
app.secret_key = 'GENERIC_KEY'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

# Blueprints
home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/')
def home_page():
    if current_user.is_authenticated:
        user_id = current_user.id
        tasks = Task.select().where(Task.user == user_id)
        return render_template('index.html', tasks=tasks)
    else:
        return redirect(url_for('user.login')) 

def blueprint_conf(app):
    app.register_blueprint(home)
    app.register_blueprint(user)
    app.register_blueprint(tasks)

blueprint_conf(app)

def db_config():
    db.connect()
    db.create_tables([User], safe=True)
    db.create_tables([Task], safe=True)

db_config()

@app.route('/')
def homepage():
    return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(debug=True)
