from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from extensions import db
from models import Expense

expense_bp = Blueprint("expense_bp", __name__)

# ---------------- GET ALL EXPENSES ----------------
@expense_bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()

    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()

    result = []
    for e in expenses:
        result.append({
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "note": e.note,
            "date": e.date.strftime("%Y-%m-%d")
        })

    return jsonify(result), 200


# ---------------- ADD EXPENSE ----------------
@expense_bp.route("/", methods=["POST"])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    expense = Expense(
        amount=data.get("amount"),
        category=data.get("category"),
        note=data.get("note", ""),
        date=datetime.utcnow(),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully"}), 201


# ---------------- UPDATE EXPENSE ----------------
@expense_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json()

    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    expense.note = data.get("note", expense.note)

    db.session.commit()

    return jsonify({"message": "Expense updated successfully"}), 200


# ---------------- DELETE EXPENSE ----------------
@expense_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted successfully"}), 200
