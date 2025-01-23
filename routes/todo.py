from flask import Flask, render_template, redirect, url_for, request, Blueprint, jsonify
from flask_login import current_user
from peewee import IntegrityError
from models.database import db, Task, User

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks.route('/create_task', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    term = request.form.get('term')

    user = current_user

    if not title or not description or not term:
        return jsonify({'status': 'error', 'message': "Please fill all fields!"})

    try:
        with db.atomic():
            Task.create(title=title, description=description, term=term, user=user)
        return redirect(url_for('home.home_page'))

    except IntegrityError as e:
        return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"An error occurred: {str(e)}"})

@tasks.route('/remove_task', methods=['POST'])
def remove_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return jsonify({'status':'error', 'message': "Task ID is required!"})

    try:
        task = Task.get_or_none(Task.id == task_id, Task.user == current_user.id)
        if not task:
            return jsonify({'status': 'error', 'message': "Task not found or does not belong to you!"})

        with db.atomic():
            task.delete_instance()
        return redirect(url_for('home.home_page'))
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Error: {str(e)}"})

@tasks.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    task = Task.get_by_id(task_id)
    return render_template('edit_task.html', task=task)

@tasks.route('/update_task', methods=['POST'])
def update_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return "Task ID not provided", 400

    try:
        edited_task = Task.get_by_id(task_id)
    except Task.DoesNotExist:
        return "Task not found", 404

    edited_task.title = request.form.get('title')
    edited_task.description = request.form.get('description')
    edited_task.term = request.form.get('term')
    edited_task.save()
    return redirect(url_for('tasks.list_tasks'))

@tasks.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return "Task ID not provided", 400

    try:
        task = Task.get_by_id(task_id)
        task.status = "Completed"
        task.save()
        return redirect(url_for('home.home_page'))
    except Task.DoesNotExist:
        return "Task not found", 404

@tasks.route('/uncomplete_task', methods=['POST'])
def uncomplete_task():
    task_id = request.form.get('task_id')
    if not task_id:
        return "Task ID not provided", 400

    try:
        task = Task.get_by_id(task_id)
        task.status = 'Active'
        task.save()
        return redirect(url_for('home.home_page'))
    except Task.DoesNotExist:
        return "Task not found", 404


@tasks.route('/list_tasks')
def list_tasks():
    tasks = Task.select().where(Task.user == current_user.id)
    return render_template('index.html', tasks=tasks)

@tasks.route('/task_status', methods=['POST'])
def task_status():
    pass
