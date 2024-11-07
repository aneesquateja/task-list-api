from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from ..db import db


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_data = request.get_json()

    try:
        new_goals = Goal.from_dict(request_data)

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goals)
    db.session.commit()

    return {"goal":new_goals.to_dict()}, 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))

    goals = db.session.scalars(query.order_by(Goal.id))
    goals_response = [goal.to_dict() for goal in goals]

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": "Goal not found"}, 404

    return {"goal": goal.to_dict()}, 200

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": "Goal not found"}, 404

    request_data = request.get_json()
    goal.title = request_data.get("title", goal.title)
    db.session.commit()

    return {"goal": {"id": goal.id, "title": goal.title}}, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": "Goal not found"}, 404

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, 200









        


