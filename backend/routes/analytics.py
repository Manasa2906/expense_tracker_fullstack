from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Expense
from extensions import db
from sqlalchemy import func

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/total", methods=["GET"])
@jwt_required()
def total_expense():
    user_id = get_jwt_identity()

    total = db.session.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter_by(user_id=user_id).scalar()

    return jsonify({"total": total})


@analytics_bp.route("/categories", methods=["GET"])
@jwt_required()
def category_expenses():
    user_id = get_jwt_identity()

    rows = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter_by(user_id=user_id)
        .group_by(Expense.category)
        .all()
    )

    return jsonify([
        {"category": c, "amount": a} for c, a in rows
    ])
