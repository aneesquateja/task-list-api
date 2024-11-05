from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    # Check for missing fields
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    # Create a new task instance
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body.get("completed_at")
    )
    db.session.add(new_task)
    db.session.commit()

    # Return the response with the new task's dictionary format
    return make_response({"task": new_task.to_dict()}, 201)

@tasks_bp.get("")
def get_all_tasks():
    # tasks = Task.query.all()  # Get all tasks from the database
    # tasks_response = [task.to_dict() for task in tasks]  # Convert each task to a dictionary
    # return tasks_response, 200
    
    sort_order = request.args.get("sort")  # Get the sort parameter from the query string
    tasks = Task.query.all()  # Get all tasks from the database

    # Sort tasks based on the sort_order
    if sort_order == "asc":
        tasks.sort(key=lambda task: task.title)
    elif sort_order == "desc":
        tasks.sort(key=lambda task: task.title, reverse=True)

    # Convert each task to a dictionary
    tasks_response = [task.to_dict() for task in tasks]
    
    return make_response(tasks_response, 200)


    

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")


    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.id} "{task.title}" successfully deleted'}, 200)

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"Task id '{task_id}' is invalid"}, 400))

    task = db.session.query(Task).filter_by(id=task_id).first()

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task







