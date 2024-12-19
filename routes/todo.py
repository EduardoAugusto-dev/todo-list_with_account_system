from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from models.database import User
from peewee import IntegrityError
from models.database import db
from models.database import Task


tasks = Blueprint('tasks', __name__, url_prefix = '/tasks')

@tasks.route('/create_task', methods=['POST'])
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        term = request.form.get('term')
        user_id = request.form.get('user_id')

        if not title or not description or not term or not user_id:
            return jsonify({'status': 'error', 'message': "please fill all fields!"})

        user = User.get_or_none(User.id == user_id)
        if not user:
            return jsonify({'status': 'error', 'message': "User not found"})

        try:
            with db.atomic():
                user = User.get(User.id == user_id)
                Task.create(title=title, description = description, term = term, user = user)
            return redirect(url_for('home.home_page'))

        except User.DoesNotExist:
            return jsonify({'status': 'error', 'message': "User not found"})
        except IntegrityError as e:
            return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"})

@tasks.route('/remove_task', methods=['POST'])
def remove_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return jsonify({'status':'error', 'message': "Task ID and User ID are required!"})

    try:
        with db.atomic():
            task = Task.get_or_none(Task.id == task_id)
            if not task:
                return jsonify({'status': 'error', 'message': "Task not found or the task are not of yours!"})

            task.delete_instance()
        return redirect(url_for('home.home_page'))
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Error: {str(e)}"})

@tasks.route('/edit_task', methods=['POST'])
def edit_task():
    pass

@tasks.route('/task_status', methods=['POST'])
def task_status():
    pass

