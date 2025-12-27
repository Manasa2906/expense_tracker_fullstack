from flask import Blueprint, request, jsonify
from extensions import db
from models.expense import Expense
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

expense_bp = Blueprint("expenses", __name__)

# ---------------- ADD EXPENSE ----------------
@expense_bp.route("", methods=["POST"])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json()

    amount = data.get("amount")
    category = data.get("category")
    note = data.get("note")

    if not amount or not category:
        return jsonify({"error": "Amount and category are required"}), 400

    expense = Expense(
        amount=amount,
        category=category,
        note=note,
        expense_date=date.today(),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully"}), 201


# ---------------- GET EXPENSES ----------------
@expense_bp.route("", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()

    expenses = Expense.query.filter_by(user_id=user_id).all()

    result = []
    for e in expenses:
        result.append({
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "note": e.note,
            "date": e.expense_date.isoformat()
        })

    return jsonify(result), 200
# ---------------- UPDATE EXPENSE ----------------
@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    expense = Expense.query.get_or_404(expense_id)

    # Authorization check
    if expense.user_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    expense.note = data.get("note", expense.note)

    db.session.commit()

    return jsonify({"message": "Expense updated successfully"}), 200
# ---------------- DELETE EXPENSE ----------------
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()

    expense = Expense.query.get_or_404(expense_id)

    # Authorization check
    if expense.user_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted successfully"}), 200
