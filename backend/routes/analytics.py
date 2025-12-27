from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.expense import Expense
from sqlalchemy import func
from datetime import date

analytics_bp = Blueprint("analytics", __name__)

# ---------------- TOTAL EXPENSE ----------------
@analytics_bp.route("/total", methods=["GET"])
@jwt_required()
def total_expense():
    user_id = get_jwt_identity()

    total = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == int(user_id)
    ).scalar()

    return jsonify({
        "total_expense": total or 0
    }), 200


# ---------------- MONTHLY SUMMARY ----------------
@analytics_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()
    today = date.today()

    results = db.session.query(
        func.strftime("%Y-%m", Expense.expense_date),
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == int(user_id)
    ).group_by(
        func.strftime("%Y-%m", Expense.expense_date)
    ).all()

    summary = []
    for month, total in results:
        summary.append({
            "month": month,
            "total": total
        })

    return jsonify(summary), 200


# ---------------- CATEGORY SUMMARY ----------------
@analytics_bp.route("/categories", methods=["GET"])
@jwt_required()
def category_summary():
    user_id = get_jwt_identity()

    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == int(user_id)
    ).group_by(
        Expense.category
    ).all()

    summary = []
    for category, total in results:
        summary.append({
            "category": category,
            "total": total
        })

    return jsonify(summary), 200
